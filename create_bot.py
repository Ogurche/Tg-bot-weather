from aiogram import Bot, Dispatcher
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(bot_token)
dp =  Dispatcher(bot, storage=storage)

