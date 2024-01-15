from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from loader import db
import sqlite3
start_router: Router = Router()

@start_router.message(Command('start'))
async def start(message: Message):
    try:
        await db.add_user(full_name=message.from_user.full_name, username=message.from_user.username, telegram_id=message.from_user.id)
        await message.answer("yangi qo'shildi")
        user = await db.select_all_users()
        await message.answer(user)
       
    except:
        await message.answer("Avvaldan bor!")
        await message.answer("Xush kelibsiz")