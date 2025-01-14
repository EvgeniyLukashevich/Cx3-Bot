import os
from datetime import datetime
import asyncio
import random
import mysql.connector
import data_base
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

dbase = quests = quests_id = None

admin = 669628282756530207

cf_role = {996841246016417962: -1,
           1010186572156641290: 0,
           1000730137731551382: 1,
           1009910414961811486: 2,
           1009928506966290442: 3,
           1001397006993985646: 4}

vpb_role = 1008289239210938518
guild_id = 996841246016417962
start_channel = 1006321073958166548
adv_channel = 996841247446683752

status = '/info'
task_string = f'что выведет в *консоль* этот код:\n'
answer_string = f'\n\nОтвет отправляй так: **/answer** *<твой вариант ответа>*'

adv_timer = 0
adv_title = 'На правах рекламы'
adv_text = f'Не дадим технологиям захватить мир! Машины должны батрачить на людей, а не наоборот. Вступай в ряды ' \
           f'ботоводов ✊\nКурсы по телеграм-ботоводству на базе библиотеки AIOgram языка Python\nЗа подробностями в ' \
           f'личку '


async def db_connection():
    global dbase
    try:
        dbase = data_base.DataBase(
            mysql.connector.connect(user='root', db='cf_bot', passwd=os.getenv('MYSQL_PWD'), host='mysql'))
        print('DB Connected... OK!')
        return dbase
    except:
        print('DB Connected... failed')
        await send_message_to_admin("База данных отвалилась")


@bot.event
async def on_ready():
    global quests, quests_id, dbase
    print('On start')
    dbase = await db_connection()
    if dbase:
        print('DB Connected... OK')
        quests = dbase.get_quest('all', '', 0)
        quests_id = dbase.get_quest('id', '', 0)


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(guild_id)
    embed = discord.Embed(title="Добро пожаловать!",
                          description=f'Эй, народ! Нас теперь {guild.member_count} :)\n\nПривет, {member.mention}. Я '
                                      f'бот канала CODE Father\'s. Пока я мало чего умею, '
                                      f'но всё впереди...\n\nЗагляни в ЛС, я там тебе кое-чего прислал',
                          color=0xCC974F)
    await bot.get_channel(start_channel).send(embed=embed)
    await member.send(
        f'Привет, {member.name}! Рады приветствовать тебя на нашем сервере. Чем мы здесь занимаемся?\nМы создаем '
        f'дружное коммьюнити из единомышленников в IT сфере. Здесь ты сможешь получить помощь с ДЗ, '
        f'получить консультацию по текущим темам от однокурсников, пообщаться в прямом эфире с крутыми гостями, '
        f'которые уже работают в IT, обменяться опытом, найти команду для реализации своих идей, да и просто '
        f'пообщаться :)\nЕсли возникнут вопросы, то пиши кому-нибудь из администараторов и тебе обязательно '
        f'ответят\n\nНо для начала было бы неплохо получить роль первого уровня (для доступа к голосовому чату и '
        f'архиву с полезными ссылками)\nДля этого просто введи на канале /access и мы с тобой всё '
        f'сделаем!\n\nПриятных тебе минут на сервере и удачного обучения!\n\nP.S. Если увидишь Джонна Конора - '
        f'передай привет')
    await send_message_to_admin(f'У нас новый участник - {member.name}!')
    await new_user(member)

@bot.command(aliases=['реклама'])
async def adverstiment(ctx, time: int):
    global dbase, adv_timer
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        adv_timer = time
    else:
        ctx.
        await ctx.send(f'Эта команда для тебя недоступна')
    while (adv_timer):
        guild = bot.get_guild(guild_id)
        member = guild.get_member(admin)
        atext = adv_text + f'{member.mention}'
        embed = discord.Embed(title=adv_title,
                              description=atext,
                              color=0x00ff7b)
        await bot.get_channel(adv_channel).send(embed=embed)
        await asyncio.sleep(adv_timer)


@bot.command(aliases=['таймер'])
async def set_adv_timer(ctx, time: int):
    global dbase, adv_timer
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        adv_timer = time
    else:
        await ctx.send(f'Эта команда для тебя недоступна')




async def new_user(member):
    global quests_id
    date = datetime.now()
    user = ((member.id, member.name, 0, 10, 0, date))
    dbase = await db_connection()
    dbase.add_item('new_user', user)


async def check_user(ctx):
    global dbase
    user = dbase.get_user('user', ctx.author.id)
    await delete_message(ctx)
    if not user: await new_user(ctx.author)
    return True


async def check_member(member):
    global dbase
    try:
        user = dbase.get_user('user', member.id)
        if not user: await new_user(member)
    except:
        await member.send(
            f'{member.mention}, твой никнейм содержит недопустимые символы. Измени никнейм, иначе мы не сможем внести '
            f'тебя в БД')
    return True


@bot.event
async def on_member_remove(member):
    global dbase
    dbase.delete_item(member.id, 'user_list')
    await send_message_to_admin(f'Нас покинул {member.name}!')


def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k


async def send_message_to_admin(text):
    guild = bot.get_guild(guild_id)
    member = guild.get_member(admin)
    await member.send(text)


async def get_user_roles(ctx):
    member_roles = [role.id for role in bot.get_guild(guild_id).get_member(ctx.message.author.id).roles]
    await delete_message(ctx)
    return member_roles


async def remove_role(member, role):
    await member.remove_roles(role)


async def delete_message(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command()
async def mailing(ctx, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        users = dbase.get_user('user_id')
        text = ''
        for word in args:
            text += f'{word} '
        for user in users:
            guild = bot.get_guild(guild_id)
            member = guild.get_member(int(user[0]))
            await member.send(text)
    else:
        await ctx.send(f'Эта команда для тебя недоступна')




@bot.command()
async def info(ctx):
    ctx.
    global dbase
    await check_user(ctx)
    user_date = dbase.get_user('date', ctx.author.id)
    guild = bot.get_guild(guild_id)
    roles = []
    [roles.append(guild.get_role(x).name) for x in await get_user_roles(ctx)]
    txt_role = ''
    txt_txt_channels = 'Текстовые каналы **Прихожая**, **Манифест**, **Важная информация**, **Флудильня**'
    txt_voice_channels = 'Голосовые каналы **Переговорная**'
    txt_advanced = ''
    txt_commands = '**/info** - помощь по боту канала CODE Father\'s\n'
    for role in roles:
        txt_role += f'{role}, '
    for role in await get_user_roles(ctx):
        match cf_role.get(role):
            case -1:
                txt_commands += '**/access** - для принятия правил(манифеста) сервера и получения серой роли\n'
            case 0:
                txt_commands += '**/task** *<выбор языка>* - для получения зеленой роли путем решения задачи на выбранном языке\n'
                txt_commands += '**/answer** *<твой ответ>* - для отправки ответа на полученную задачу *(**Важно!** Ответы False и false - разные вещи. Вводи именно так, как требует задача.)*\n'
            case 1:
                txt_txt_channels += ', **Полезные ссылки**, **Документация**, **Podcasts**, **Вопросы для гостя**'
                txt_voice_channels += ', **Кабинеты языков**, **Podcast**'
                pass
            case 2:
                txt_advanced += 'Создавать свою **Семью** и получаешь доступ к текстовому и голосовму каналу своей семьи '
            case 3:
                pass
            case 4:
                txt_txt_channels += ', **Штаб**'
                txt_voice_channels += ', **Штаб**'
                txt_advanced += ', выдавать и снимать роли, участвовать в совещании штаба CF '
                txt_commands += '**/embed** *<Цвет> <Заголовок> <Текст сообщения>* - цвет в HEX формате, если в заголовке больше одного слова, то обязательно в двойных кавычках, текст сообщения - сколько угодно\n'
                txt_commands += '**/poll** *<Цвет> <Вопрос> <Варианты ответов>* - цвет в HEX формате, если в вопросе больше одного слова, то обязательно в двойных кавычках, варианты ответов одним словом\n'
                txt_commands += '**/set_task** *<пользователь> <номер задачи>* - выдать пользователю новую задачу, пользователя можно задать кликнув по нему правой кнопкой и выбрать *Упомянуть*'
    await ctx.author.send(
        f'{(ctx.author.mention)}, на сервере CODE Father\'s ты провел {str(datetime.now() - user_date[0])[:-7]}\nУ тебя есть роли:\n{txt_role[:-2]}.\n\n**Тебе доступно:**\n{txt_txt_channels}\n{txt_voice_channels}\n{txt_advanced}\n\n**И ты можешь использовать следующие команды бота:**\n{txt_commands}')


@bot.command()
async def set_task(ctx, stat_name: str, stat):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        dbase.update_item('set_task', stat_name[2:-1], stat)
        await ctx.send(
            f'У пользователя {stat_name} теперь {stat} задача')
    else:
        await ctx.send(f'Эта команда для тебя недоступна')


@bot.command()
async def family(ctx, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        dbase.update_item('set_family', args[0][2:-1], args[1])
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(args[1]))
        role2 = guild.get_role(int(get_key(cf_role, 4)))
        member = guild.get_member(int(str(args[0])[2:-1]))
        await member.add_roles(role)
        await member.add_roles(role2)
        await ctx.send(
            f'Поздравляю, {member}! Теперь ты глава семьи {role}!')
    elif int(dbase.get_user('family', ctx.author.id)[0]) in await get_user_roles(ctx):
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(dbase.get_user('family', ctx.author.id)[0]))
        member = guild.get_member(int(str(args[0])[2:-1]))
        await member.add_roles(role)
        await ctx.send(
            f'Поздравляю, {member}! Теперь ты в семье {role}!')
    else:
        await ctx.send(f'Эта команда для тебя недоступна')


@bot.command()
async def embed(ctx, color, title, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        text = ''
        for word in args:
            text += f'{word} '
        await check_user(ctx)
        col = int(str(color).replace('#', ''), 16)
        embed = discord.Embed(color=col, title=title, description=f'{text}')
        await ctx.send(embed=embed)
        await delete_message(ctx)
    else:
        await ctx.send(f"У тебя нет доступа к этой команде")


@bot.command(aliases=["голосование", "голос"])
async def poll(ctx, color, question, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        numbers = []
        [numbers.append(f'{i}\uFE0F\u20E3') for i in range(1, 11)]
        if len(args) <= 10:
            col = int(str(color).replace('#', ''), 16)
            embed = discord.Embed(title="Голосование", description=question, color=col)
            fields = [("Варианты:", "\n".join([f'{numbers[idx]} - {option}' for idx, option in enumerate(args)]), True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)
            for emoji in numbers[:len(args)]:
                await message.add_reaction(emoji)
        await delete_message(ctx)
    else:
        await ctx.send(f"У тебя нет доступа к этой команде")


@bot.command()
async def add_all_user_to_db(ctx, *args, **kwargs):
    guild = bot.get_guild(guild_id)
    members = guild.members
    for each in members:
        await check_member(each)


@bot.command()
async def clear_all_users_role(ctx, *args, **kwargs):
    global dbase
    await delete_message(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        guild = bot.get_guild(guild_id)
        role = guild.get_role(get_key(cf_role, int(args[0])))
        members = guild.members
        for each in members:
            if role in each.roles:
                await each.remove_roles(role)
    else:
        await ctx.send(f'{ctx.author.mention}, у тебя нет прав для использования этой команды')


@bot.command()
async def access(ctx, *args, **kwargs):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 0) in await get_user_roles(ctx):
        await ctx.send(
            f'{ctx.author.mention}, ты уже принял правила сервера. Для помощи по командам бота используй **/info**')
    else:
        guild = bot.get_guild(guild_id)
        npc_role = guild.get_role(get_key(cf_role, 0))
        member = guild.get_member(ctx.message.author.id)
        await member.add_roles(npc_role)
        await ctx.send(
            f'{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня! Командой **/info** можешь узнать свои новые возможности')


@bot.command()
async def task(ctx, *args, **kwargs):
    global dbase
    dbase = await db_connection()
    await check_user(ctx)
    if args == ():
        user_task = dbase.get_user('task', ctx.author.id)
        if not user_task[0] == str(0):
            user_quest = dbase.get_quest('task', user_task[0][0], int(user_task[0][1]))
            await ctx.send(f'{ctx.author.mention}, {task_string}{user_quest[0]}{answer_string}')
        else:
            await ctx.send(
                f'{ctx.author.mention}, для начала тебе нужно взять задачу при помощи команды **/task** *<язык>*, языки p - Python, j - Java, c - C#')
    else:
        if get_key(cf_role, 1) in await get_user_roles(ctx):
            await ctx.send(
                f'{ctx.author.mention}, у тебя уже есть роль первого уровня. Для помощи по командам бота используй **/info**')
        elif args[0] not in ('p', 'j', 'c'):
            await ctx.send(f'{ctx.author.mention}, введи язык корректно.  p - Python, j - Java, c - C#')
        else:
            letter = args[0]
            number = random.choice([1, 2, 3, 4, 5])
            dbase.update_item('set_task', ctx.author.id, str(letter) + str(number))
            user_quest = dbase.get_quest('task', letter, int(number))
            await ctx.send(f'{ctx.author.mention}, {task_string}{user_quest[0]}{answer_string}')


@bot.command()
async def answer(ctx, *args, **kwargs):
    global dbase, quest_answers
    dbase = await db_connection()
    await check_user(ctx)
    if not args == ():
        guild = bot.get_guild(guild_id)
        new_role = guild.get_role(get_key(cf_role, 1))
        old_role = guild.get_role(get_key(cf_role, 0))
        member = guild.get_member(ctx.message.author.id)
        task = dbase.get_user('task', ctx.author.id)
        if str(args[0]) == str(dbase.get_quest('answer', task[0][0], task[0][1])[0]):
            await delete_message(ctx)
            await member.add_roles(new_role)
            await ctx.send(
                f"{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня! Командой **/info** можете узнать свои новые возможности")
            await remove_role(member, old_role)
        else:
            await delete_message(ctx)
            await ctx.send(
                f'{ctx.author.mention}, ну чего-то ты не то написал. Разберись для начала с этим, а потом уже роль')


async def game_info():
    global status
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game('/info'))
        await asyncio.sleep(15)


# bot.loop.create_task(game_info())
bot.run(os.getenv('TOKEN'))