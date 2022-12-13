from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot("5829943629:AAG3QQu-TeiWSjuppG0wtYQUAQutp54KklU")
dp = Dispatcher(bot, storage=MemoryStorage())

