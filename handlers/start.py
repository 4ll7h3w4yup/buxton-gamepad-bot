from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from utils.database import get_user_by_telegram_id, register_user

async def cmd_start(message: types.Message):
    user = get_user_by_telegram_id(message.from_user.id)

    if not user:
        photos = await message.from_user.get_profile_photos()
        avatar_url = photos.photos[0][0].file_id if photos.total_count > 0 else None

        register_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            avatar_url=avatar_url
        )
        await message.answer(f"👋 Добро пожаловать, {message.from_user.first_name}!\nТы успешно зарегистрирован!")
    else:
        await message.answer(f"👋 С возвращением, {message.from_user.first_name}!")

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
