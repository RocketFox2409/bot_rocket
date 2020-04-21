"""Made by RocketFox
   ты не станешь КРУТЫМ ПРОГРАММИСТОМ если
   просто скопируешь его!"""

import discord
from discord import utils
from discord.ext import commands 
from datetime import datetime
import config  # ТОКЕН!!!, ид канала
import os
import pytz

__version__ = '1.0.9'

__timezone__ = "Asia/Omsk"

# переменные
Bot_id = 699840979942899752
LOG_ID = config.LOG_ID
Auth_id = config.AUTH_ID
pred_id = config.PRED_ID
ADMIN_LIST = config.ADMIN_LIST
# TOKEN = config.TOKEN

bot = commands.Bot(command_prefix=">")  # префикс для комманд

tz = pytz.timezone(__timezone__)

def time(d):  # функиция получения времени
    a = datetime.now(tz)  # дата сейчас
    if d == 1:  # time(1) возращает ч:м
        a = a.strftime("%H:%M")
    elif d == 2:
        a = a.strftime("%d.%m.%Y  %H:%M:%S")  # time(2) возращает д:м:г ч:м:с
    else:
      a = a.strftime("%H:%M:%S %d.%m.%Y")  # time(2) возращает ч:м:с д:м:г
    return a
    

print("Подключение...")

@bot.event
async def on_ready():
    stat = "Бот запущен" + "\nВерсия бота: " + __version__ + "\nВремя запуска ("+__timezone__+"): " + time(2)
    print("""+-+-+-+-+-+-+-+-+-+\n|R|o|c|k|e|t|F|o|x|\n+-+-+-+-+-+-+-+-+-+""")
    print(stat)  # Статус в терминал
    await bot.get_channel(LOG_ID).send(f"``` {stat} ```")  # Статус в лог канал
    await bot.change_presence(activity=discord.Game(f'Был запущен в {time(3)}'))


@bot.event
async def on_member_join(member):
    x = member.guild.members  # список юзеров на сервере
    await member.send(f"Ку епта {member.name} для получения всех прав пройдите в канал #⚡аутентификация!!")
    await bot.get_channel(LOG_ID).send(f"Пресоединился новый участник {member.name}#{member.discriminator}")
    await bot.get_channel(701426151704494080).edit(name= f"Пользователей: {len(x)}")
    await bot.get_channel(701435569309483098).edit(name= member.name)
    role = discord.utils.get(member.guild.roles, name=config.ROLE_REG_1)
    await member.add_roles(role)


@bot.event
async def on_message(message):  # если пришло сообщения
    await bot.process_commands(message)  # обработчик команд
    if message.channel.id == Auth_id and message.author.id != Bot_id:  # добовление реакций в канал аутентификация
        await bot.get_channel(LOG_ID).send(f'Участник {message.author} ({message.author.display_name}) подал заявку в {time(1)} на аутентификацию')
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    if message.channel.id == pred_id and message.author.id != Bot_id:  # добовление реакций в канал предложения
        await bot.get_channel(LOG_ID).send(f'Участник {message.author} ({message.author.display_name}) написал предложения или жалабу в {time(1)}')
        await message.add_reaction("✅")
        await message.add_reaction("❎")
        # await message.add_reaction("<:Warzone2100:693087501220446248>")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == Auth_id:  # Проверка добавлина ли рекция на канал
        channel = bot.get_channel(payload.channel_id)  # получение канала сообщения
        message = await channel.fetch_message(payload.message_id)  # ид сообщения
        author = message.author  # автор
        message_text = message.content

        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(author.id)

        member_1 = guild.get_member(payload.user_id)

        if payload.user_id in ADMIN_LIST:
            if payload.emoji.name == '👍':
                x = message_text.split(" ")
                x1 = x[1]
                x2 = x1[:-3] 
                x3 = x[3] + " | " + x2
                await author.edit(nick =x3) # изменение ника
                await bot.get_channel(LOG_ID).send(f'Заявка для {author} ({author.display_name}) одобрена {time(2)}')  # Статус в лог канал
                role = discord.utils.get(member.guild.roles, name=config.ROLE_REG)
                await member.add_roles(role)  # добовления роли
                role_1 = discord.utils.get(member.guild.roles, name=config.ROLE_REG_1)
                await member.remove_roles(role_1)  # удоления роли
            else:
                await member.send(f'Ваша заявка не одобрена')
                await bot.get_channel(Auth_id).send(f'Заявка для {author} ({author.display_name}) не одобрена')  # Статус в лог канал
        else:
            if payload.user_id != Bot_id:
                await message.remove_reaction(payload.emoji, member_1)


@bot.command()
async def D(ctx):
    i = 0
    for user in ctx.guild.members:
        # print(f"{user.name}#{user.discriminator} Статус: {user.status}")
        if user.status != discord.Status.offline:
            i +=1
            print (f"{user.name}#{user.discriminator} Статус: {user.status}")       
    print(i)


@bot.command()
async def web(ctx):
    author = ctx.message.author
    try:
        await author.send(f"https://discordapp.com/channels/{author.guild.id}/{author.voice.channel.id}")
    except:
        await author.send("Вы не находитесь в голосовом канале")


# @bot.command()
# async def clear(ctx, amount: int):
    # await ctx.channel.purge(limit= amount)
    # await ctx.send(f"Удалено {amount} сообщений")


token = os.environ.get("BOT_TOKEN")
bot.run(str(token))  # ТОКЕННН!
