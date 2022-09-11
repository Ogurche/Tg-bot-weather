from aiogram import  executor
from create_bot import dp 
from handlers import main
from database import sqlit


async def on_startup(_):
    print ("Я готов, Поехали!")

main.registr_handlers(dp)


executor.start_polling(dp,skip_updates=True, on_startup=on_startup)