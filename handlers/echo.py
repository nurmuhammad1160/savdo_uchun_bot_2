from aiogram import Router
from aiogram.types import Message
from loader import db
import sqlite3
router: Router = Router()


@router.message()
async def process_any_message(message: Message):
    
        
    await message.reply(text=message.text)
