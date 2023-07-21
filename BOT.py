from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
import nest_asyncio
import sqlite3
from sqlite3 import Error
import time

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import random


con=sqlite3.connect('places baza.db')
cur=con.cursor()



nest_asyncio.apply()

bot = Bot(token='') # Токен приложен в заявке, его нужно скопировать и вставить в кавычки в этой строке. Пример: bot = Bot(token='СЮДА')
dp = Dispatcher(bot, storage=MemoryStorage())

class AddState(StatesGroup):
    title= State()
    photo = State()
    geo = State()
    desk =State()
    dist = State()


pictures={
    0:'https://static.wikia.nocookie.net/roleyplay/images/8/8a/%D0%9F%D0%BE%D0%B4%D0%B7%D0%B5%D0%BC%D0%B5%D0%BB%D1%8C%D0%B5_1.jpg/revision/latest?cb=20161031144352&path-prefix=ru',
    1:'https://upload.wikimedia.org/wikipedia/commons/e/ed/St_Leonard_lake.jpg',
    2:'https://oir.mobi/uploads/posts/2019-12/1575753389_6-10.jpg'
}

district = {
    'so' : ['Северный', 'Зеленая Роща', 'Партизана Железняка', 'Взлётка'],
    'cn' : ['Покровка', 'Центр'],
    'ok' : ['Ветлужанка', 'Студгородок', 'Академгородок', 'Октябрьский'],
    'sv' : ['Предмостная площадь', 'Центр Свердловского', 'Базаиха']
}



centralPh = {
    '1' : 'https://masterskating.ru/wp-content/uploads/2021/04/katok-v-tsentralnom-parke-krasnoyarska_3.jpeg',
    '2' : 'https://snowyowlhotel.ru/upload/iblock/598/naberezhnaya_eniseya.jpg',
    '3' : 'https://vsegda-pomnim.com/uploads/posts/2022-03/1648635441_12-vsegda-pomnim-com-p-ostrov-tatisheva-krasnoyarsk-foto-14.jpg'
}

centrtxt = {
    '1' : 'Если вы хотели ощутить себя как в новогоднем фильме, вам точно нужно на каток в Парке Горького!',
    '2' : 'Классика.. Красноярская левобережная набережная! Главное, одевайтесь теплее :)',
    '3' : 'Чтобы насладиться природой не обязательно выезжать за город! Остров Татышев – огромный парк, где вы найдете различные спортивные площадки, яблоневые сады, секретные тропинки и, конечно же, сусликов!'
}

centrGeo = {
    '1' : ['56.008402','92.851172'], 
    '2' : ['56.006352', '92.868208'],
    '3' : ['56.027052', '92.943328']
}




    
sp = cur.execute('SELECT ID FROM places').fetchall()
countPlace = len(sp)
print('Здравствуйте. Доступно мест:', countPlace)


button1 = KeyboardButton('Железнодорожный')
button2 = KeyboardButton('Кировский')
button3 = KeyboardButton('Ленинский')
button4 = KeyboardButton('Октябрьский')
button5 = KeyboardButton('Свердловский')
button6 = KeyboardButton('Советский')
button7 = KeyboardButton('Центральный')

markup = ReplyKeyboardMarkup(one_time_keyboard=True).add(button1).add(button2).add(button3).add(button4).add(button5).add(button6).add(button7)

kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Найти места рядом',callback_data='1'),
    InlineKeyboardButton('Предложить место',callback_data='send'))




kgeo=types.InlineKeyboardMarkup()
ke=types.InlineKeyboardMarkup()
areas=types.InlineKeyboardMarkup()

areas.add(types.InlineKeyboardButton('Железнодорожный', callback_data='zd'))
areas.add(types.InlineKeyboardButton('Кировский', callback_data='kr'))
areas.add(types.InlineKeyboardButton('Ленинский', callback_data='ln'))
areas.add(types.InlineKeyboardButton('Октябрьский', callback_data='ok'))
areas.add(types.InlineKeyboardButton('Свердловский', callback_data='sv'))
areas.add(types.InlineKeyboardButton('Советский', callback_data='so'))
areas.add(types.InlineKeyboardButton('Центральный', callback_data='cn'))
areas.add(types.InlineKeyboardButton('Не важно', callback_data='any'))
# areas.add(types.InlineKeyboardButton('Отправлю геопозицию)', callback_data='2'))



zenSoviet=types.InlineKeyboardMarkup()
zenSoviet.add(types.InlineKeyboardButton('Северный', callback_data='nor'))
zenSoviet.add(types.InlineKeyboardButton('Зеленая Роща', callback_data='rosh'))
zenSoviet.add(types.InlineKeyboardButton('Партизана Железняка',callback_data='pzh'))
zenSoviet.add(types.InlineKeyboardButton('Взлётка',callback_data='vzl'))

zenCent = types.InlineKeyboardMarkup()
zenCent.add((types.InlineKeyboardButton('Покровка', callback_data='pokr')))
zenCent.add((types.InlineKeyboardButton('Центр', callback_data='centr')))

zenOkt = types.InlineKeyboardMarkup()
zenOkt.add((types.InlineKeyboardButton('Ветлужанка', callback_data='vetl')))
zenOkt.add((types.InlineKeyboardButton('Студгородок', callback_data='stud')))
zenOkt.add((types.InlineKeyboardButton('Академгородок', callback_data='akad')))
zenOkt.add((types.InlineKeyboardButton('Октябрьский', callback_data='okt')))

zenSver = types.InlineKeyboardMarkup()
zenSver.add((types.InlineKeyboardButton('Предмостная площадь', callback_data='predmost')))
zenSver.add((types.InlineKeyboardButton('Центр Свердловского', callback_data='cesv')))
zenSver.add((types.InlineKeyboardButton('Базаиха', callback_data='bzh')))
kgeo.add(types.InlineKeyboardButton('Давайте',callback_data='3'))
kgeo.add(types.InlineKeyboardButton('Случайное место',callback_data='random'))
# kgeo.add(types.InlineKeyboardButton('Отправить геопозицию',callback_data='2'))
# kgeo.add(types.InlineKeyboardButton('Не хочу отправлять геопозицию',callback_data='3'))
# ke.add(types.InlineKeyboardButton('Все таки я не хочу отправлять геопозицию...',callback_data='3'))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  await message.answer('Привет, готов гулять с нами?', reply_markup=kb)



# @dp.callback_query_handler()
# async def user_answer(call):
# global k


k = 0

@dp.callback_query_handler()
async def ans(call):
  if call.data == '1':
    await call.message.answer('Для начала давай уточним, где ты находишься?', reply_markup=kgeo)
  elif call.data == '2':
    await call.message.answer('Отлично, нажми на значок скрепки и выбери "геопозиция"', reply_markup=ke)
  elif call.data == '3':
    await call.message.answer('Хорошо, в каком районе ты сейчас?', reply_markup=areas)
  elif call.data=='send':
     await call.message.answer('Введите название места!')
     await AddState.title.set() 

  elif call.data == 'so':
    await call.message.answer('Так... Еще пару вопросов',reply_markup=zenSoviet)
  elif call.data == 'cn':
    await call.message.answer('Так... Еще пару вопросов',reply_markup=zenCent)
    # places(call.data)
  # elif call.data == 'ok':
  #   await call.message.answer('Так... Еще пару вопросов',reply_markup=zenOkt)
  elif call.data == 'sv':
    await call.message.answer('Так... Еще пару вопросов',reply_markup=zenSver)

  # async def sendPlace(ID):
  #   photo = cur.execute(f'SELECT photo FROM places WHERE ID = {ID}').fetchall()[0][0]
  #   caption = cur.execute(f'SELECT desk FROM places WHERE ID = {ID}').fetchall()[0][0]
  #   geo = cur.execute(f'SELECT geo FROM places WHERE ID = {ID}').fetchall()[0][0]

  #   index = geo.find(', ')
  #   lat = geo[:index]
  #   long = geo[index + 2:]
  #   await bot.send_photo(call.message.chat.id, photo=photo, caption=caption)
  #   await bot.send_location(call.message.chat.id, lat, long)

  global k

  ques = types.InlineKeyboardMarkup()
  ques.add(types.InlineKeyboardButton('Давайте)', callback_data=call.data))

  datas = ['nor', 'rosh', 'pzh', 'vzl', 'pokr', 'centr', 'vetl', 'stud', 'akad', 'okt', 'predmost', 'cesv', 'bzh', 'any', 'zd', 'kr', 'ln', 'ok']
  # global ID  

  if call.data == 'random':
    ID = random.randint(1, countPlace)
    photo = cur.execute(f'SELECT photo FROM places WHERE ID = {ID}').fetchall()[0][0]
    title = cur.execute(f'SELECT title FROM places WHERE ID = {ID}').fetchall()[0][0]
    caption = f'*{title}*\n' + cur.execute(f'SELECT desk FROM places WHERE ID = {ID}').fetchall()[0][0]
    geo = cur.execute(f'SELECT geo FROM places WHERE ID = {ID}').fetchall()[0][0]
    index = geo.find(', ')
    lat = geo[:index]
    long = geo[index + 2:]
    await bot.send_photo(call.message.chat.id, photo=photo, caption=caption,parse_mode='Markdown')
    time.sleep(0.5)
    await bot.send_location(call.message.chat.id, lat, long)

    if k < countPlace - 1:
      time.sleep(0.5)
      await bot.send_message(call.message.chat.id,'Хотите посмотреть ещё?', reply_markup=ques)
      k += 1
    else:
      time.sleep(0.5)
      await call.message.answer('Места в этой категории закончились.. Если ничего не понравилось, попробуй выбрать другие районы 😘', reply_markup=areas)
      k = 0

  if call.data in datas:
    
    # def refresh():
    #   global ID
    #   ID = cur.execute(f'SELECT ID FROM places WHERE mkrn = "{call.data}"').fetchall()[k][0]
    # refresh()
    # print(ID)
    
    # sendPlace(ID)
    print(k)
    ID = cur.execute(f'SELECT ID FROM places WHERE mkrn = "{call.data}"').fetchall()[k][0]
    idlist = cur.execute(f'SELECT ID FROM places WHERE mkrn = "{call.data}"').fetchall()
    print(idlist)
    photo = cur.execute(f'SELECT photo FROM places WHERE ID = {ID}').fetchall()[0][0]
    title = cur.execute(f'SELECT title FROM places WHERE ID = {ID}').fetchall()[0][0]
    caption = f'*{title}*\n' + cur.execute(f'SELECT desk FROM places WHERE ID = {ID}').fetchall()[0][0]
    geo = cur.execute(f'SELECT geo FROM places WHERE ID = {ID}').fetchall()[0][0]

    index = geo.find(', ')
    lat = geo[:index]
    long = geo[index + 2:]
    await bot.send_photo(call.message.chat.id, photo=photo, caption=caption,parse_mode='Markdown')
    time.sleep(0.5)
    await bot.send_location(call.message.chat.id, lat, long)
    

    
    if k < len(idlist) - 1:
      time.sleep(0.5)
      await bot.send_message(call.message.chat.id,'Хотите посмотреть ещё?', reply_markup=ques)
      k += 1
    else:
      time.sleep(0.5)
      await call.message.answer('Места в этой категории закончились.. Если ничего не понравилось, попробуй выбрать другие районы 😘', reply_markup=areas)
      k = 0
    
    
@dp.message_handler(state=AddState.title)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Отправьте фото')
    await AddState.next()

@dp.message_handler(content_types=['photo'],state=AddState.photo)
async def get_id(message: types.Message, state: FSMContext):
    # await message.photo[-1].download()
    # await state.update_data(photo=message.photo[-1].file_id)
    photoSize = message.photo[-1]
    file_info = await bot.get_file(photoSize.file_id)
    fileExt = file_info.file_path.split(".")[-1]
    await message.photo[-1].download(destination_file=f"{photoSize.file_unique_id}.{fileExt}")
    await state.update_data(photo=f"{photoSize.file_unique_id}.{fileExt}")
    await message.answer('Отправь геолокацию места')
    await AddState.next()

@dp.message_handler(content_types=['location'],state=AddState.geo)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(geo=str(message.location.latitude)+", "+str(message.location.longitude))
    await message.answer('Отправь описание')
    await AddState.next()

@dp.message_handler(state=AddState.desk)
async def get_id(message: types.Message, state: FSMContext):
    await state.update_data(desk=message.text)
    await message.answer('Отправь район', reply_markup=markup)
    await AddState.next()

@dp.message_handler(state=AddState.dist)
async def get_id(message: types.Message, state: FSMContext):
    print(message.text)
    if message.text == 'Железнодорожный':
      await state.update_data(dist='zd')
    elif message.text == 'Кировский':
      await state.update_data(dist='kr')
    elif message.text == 'Ленинский':
      await state.update_data(dist='ln')
    elif message.text == 'Октябрьский':
      await state.update_data(dist='ok')
    elif message.text == 'Свердловский':
      await state.update_data(dist='sv')
    elif message.text == 'Советский':
      await state.update_data(dist='so')
    elif message.text == 'Центральный':
      await state.update_data(dist='cn')
    elif message.text == 'Не важно':
      await state.update_data(dist='any')
    data = await state.get_data()
    cur.execute(f"INSERT INTO recs (title,photo,geo,desk,dist,mkrn,user_id) VALUES (?,?,?,?,?,?,?)",(data['title'],data['photo'],data['geo'],data['desk'],data['dist'],None,message.from_user.id))
    con.commit()
    await message.answer('Данные отправлены')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши /start")


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
