from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Ввести дату рождения", callback_data="start_process_birth_data")],
                [
                    InlineKeyboardButton(text="Менеджер", callback_data="call_to_manager"),
                    InlineKeyboardButton(text="Примеры работ", callback_data="job_examples")
                ],
                [InlineKeyboardButton(text="Все камни",
                                      callback_data="watch_all_gems"), ],
            ]
)