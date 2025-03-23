import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start
from utils.postback import start_postback_server

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация хендлеров
    start.register_handlers(dp)

    # Параллельно запускаем postback-сервер и бота
    await asyncio.gather(
        dp.start_polling(bot),
        start_postback_server()
    )

if __name__ == '__main__':
    asyncio.run(main())
