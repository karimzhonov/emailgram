from aiogram import types as _types
from aiogram import Bot as _Bot
from aiogram import Dispatcher as _Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage as _MemoryStorage
from config import TOKEN


bot = _Bot(TOKEN, parse_mode=_types.ParseMode.HTML)
storage = _MemoryStorage()
dp = _Dispatcher(bot, storage=storage)
