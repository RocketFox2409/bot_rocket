import config  # ид канала
import os, sys, pytz, asyncio, discord
from discord import utils
from discord.ext import commands 
from datetime import datetime

__version__ = '1.1.2'

__timezone__ = "Asia/Omsk"

tz2 = pytz.timezone("Europe/Moscow")


# переменные
stat = 0
Bot_id = 699840979942899752
LOG_ID = config.LOG_ID # канал для логов
pred_id = config.PRED_ID # канал предложений
ADMIN_LIST = config.ADMIN_LIST # лист админов


bot = commands.Bot(command_prefix="E!")  # префикс для комманд

tz = pytz.timezone(__timezone__)


def time(d):  # функиция получения времени
    a = datetime.now(tz)  # дата сейчас
    time2 = datetime.now(tz2)
    if d == 1:  # time(1) возращает ч:м
        a = a.strftime("%H:%M")
    elif d == 2:
        a = a.strftime("%d.%m.%Y  %H:%M:%S")  # time(2) возращает д:м:г ч:м:с
    elif d == 9:
        a = time2.strftime("%H:%M")
    elif d == 8:
        a = time2.strftime("%d.%m")
    else:
      a = a.strftime("%H:%M:%S %d.%m.%Y")  # time(3) возращает ч:м:с д:м:г
    return a
    

print(f"Подключение({sys.platform})...")

@bot.event
async def on_ready():
    stat = "Бот запущен" + "\nВерсия бота: " + __version__ + "\nВремя запуска ("+__timezone__+"): " + time(2) +"\n" + sys.platform
    print("""+-+-+-+-+-+-+-+-+-+\n|R|o|c|k|e|t|F|o|x|\n+-+-+-+-+-+-+-+-+-+""")
    print(stat)  # Статус в терминал
    await bot.get_channel(LOG_ID).send(f"``` {stat} ```")  # Статус в лог канал
    await bot.change_presence(activity=discord.Game(f'Был запущен в {time(3)}'))



@bot.event
async def on_member_join(member):
    x = member.guild.members  # список юзеров на сервере {member.name}
    
    await member.send(f"""Добро пожаловать уважаемый {member.name} на наш уютный сервер - на этом сервере вы сможете найти себе занятие, только ведите себя хорошо и не пересекай черту правил
Найдете с кем можно будет поиграть в ту или иную игру; тут есть много разных людей, и со многими вы сможете подружиться или просто пообщаться; 
Администрация желает вам приятного времяпрепровождения...""")

    await bot.get_channel(LOG_ID).send(f"Пресоединился новый участник `{member.name}#{member.discriminator}`")
    await bot.get_channel(701426151704494080).edit(name= f"Участников: {len(x)}")
    await bot.get_channel(701435569309483098).edit(name= member.name)
    role = discord.utils.get(member.guild.roles, id=693060312118591488)
    await member.add_roles(role)


@bot.event
async def on_member_remove(member):
    x = member.guild.members  # список юзеров на сервере {member.name}
    await bot.get_channel(701426151704494080).edit(name= f"Участников: {len(x)}")
    await bot.get_channel(LOG_ID).send(f"Ушел участник `{member.name}#{member.discriminator}`")


@bot.event
async def on_message(message):  # если пришло сообщения
    await bot.process_commands(message)  # обработчик команд
    if message.channel.id == pred_id and message.author.id != Bot_id:  # добовление реакций в канал предложения
        await bot.get_channel(LOG_ID).send(f'Участник {message.author} ({message.author.display_name}) написал предложения или жалабу в {time(3)}')
        await message.add_reaction("✅")
        await message.add_reaction("❎")


@bot.event
async def on_member_update(before, after):
    global stat
    stat += 1
    if stat > 2:
        await bot.get_channel(717330360949669919).edit(name= f"Дата: {time(8)}")
        stat = 0
        i = 0
        channel = bot.get_channel(693056342440804404)  # получение канала сообщения
        message = await channel.fetch_message(703894824813592646)  # ид сообщения
        users = []
        users.append("Список пользоватлей в сети")
        for user in after.guild.members:
            if user.status != discord.Status.offline:
                i += 1
                users.append(f"{user.display_name}&&({user}) Статус: {config.USER_STAT[str(user.status)]}")
        users.append(f"Пользоватлей в сети на сервере: {i}")
        await bot.get_channel(703576114723029163).edit(name= f"В сети: {i}")
        await message.edit(content = "\n".join(users))


@bot.command()
async def web(ctx):
    author = ctx.message.author
    await ctx.message.delete()
    try:
        await author.send(f"https://discordapp.com/channels/{author.guild.id}/{author.voice.channel.id}")
    except:
        await author.send("Вы не находитесь в голосовом канале")


@bot.command()
@commands.is_owner()
async def embed(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0x0c0c0c))


@bot.command()
async def server(ctx):
    await ctx.message.delete()
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"Сервер `{ctx.guild.name}`", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f":flag_white: **Регион: `{ctx.guild.region}`**\n\n"
        f":cowboy:  **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f":tools: **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f":green_circle: **Онлайн: `{online}`**\n\n"
        f":black_circle: **Оффлайн: `{offline}`**\n\n"
        f":yellow_circle: **Отошли: `{idle}`**\n\n"
        f":red_circle: **Не трогать: `{dnd}`**\n\n"
        f":shield: **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f":musical_keyboard: **Всего каналов: `{allchannels}`**\n\n"
        f":loud_sound: **Голосовых каналов: `{allvoice}`**\n\n"
        f":keyboard: **Текстовых каналов: `{alltext}`**\n\n"
        f":briefcase: **Всего ролей: `{allroles}`**\n\n"
        f":slight_smile: **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: {ctx.guild.name}")
    await ctx.send(embed=embed)


@bot.command()
async def google(ctx, *, question):
    try:
        url = 'https://google.gik-team.com/?q=' + str(question).replace(' ', '+')
        await ctx.send(f'Так как кое кто не умеет гуглить , я сделала это за него.\n{url}')
    except:
        await ctx.send("Ошибка")

@bot.command()
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    emb = discord.Embed(
        title= 'Текущий пинг',
        description= f'{bot.ws.latency * 1000:.0f} ms',
        color = 0x00ffff
    )
    await ctx.send(embed=emb)

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.message.delete()
    emd = discord.Embed(colour= 0x19ff19, title= f"Перезагрузка бота.....")
    emd.set_author(name= "Выполнено")
    emd.set_footer(text= "Enotik")
    await ctx.send(embed=emd)
    msg = "> :recycle: **Enotik | Перезагружен**"
    await bot.get_channel(LOG_ID).send(msg)
    os.execl(sys.executable, sys.executable, * sys.argv)


@bot.command()
@commands.is_owner()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit= amount)
    await ctx.send(f"Удалено {amount} сообщений")


token = os.environ.get("BOT_TOKEN")
bot.run(str(token))  # ТОКЕННН!
