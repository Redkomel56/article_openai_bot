from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import environs

env = environs.Env()
env.read_env()
token = env.str("BOT_TOKEN")
openai_token = env.str("OPENAI_API_KEY")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
