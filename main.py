import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MediaGroup, InputMediaVideo
from aiogram.utils import executor

import markups
from config import dp, bot
from horoscope_data import zodiacs_dates_data, zodiacs, zodiacs_messages_data, max_day_in_months_data, numbers_months, \
    gem_photos, gem_nums_photos


class GetTextData(StatesGroup):
    get_date_of_the_birth = State()


# def get_zodiac_numbers(zodiac):
#     print(['\', \''.join(zodiac_signs_data[zodiac]["dekads"][i]) for i in range(1, 4, 1)])
#
#
# get_zodiac_numbers("Козерог")

videos = (
    "BAACAgIAAxkBAAPFY4xyqDOfCSTiyPM_dw-EK0sx-voAAv4iAALdtGFI_hkXTrBnLWIrBA",
    "BAACAgIAAxkBAAPEY4xyqBtfPoQDgH7BBRk3hzKPfMcAAv0iAALdtGFI9KIOhxOrddsrBA",
    "BAACAgIAAxkBAAPGY4xy9nabyJXCQpCdRfemnldBK84AAyMAAt20YUiQpCNKsTZiRSsE",
    "BAACAgIAAxkBAAPHY4xzEc3MOVsGSwvMnVPx6gKXNBcAAgIjAALdtGFIK2QkWNwYnIsrBA",
    "BAACAgIAAxkBAAPIY4xzLRoGg-J57vVIbtRyCY-ifaAAAgQjAALdtGFITxZCa1EGPf0rBA"
    "BAACAgIAAxkBAAPJY4xzQqu2Mubr_RBK5QvIgLpgfggAAgYjAALdtGFIHrCX2E9N9j8rBA",
    "BAACAgIAAxkBAAPKY4xzVmKWVU_8FDOIhkmsPi1z8EUAAgcjAALdtGFImrdSXGhbIVYrBA",
    "BAACAgIAAxkBAAPLY4xzbtoRF5cp3BILCXynX--RSdQAAggjAALdtGFIEFWY7YHDMO4rBA",
    "BAACAgIAAxkBAAPMY4xzf4rDIRuhY-b47ETY39Y0Jb0AAgkjAALdtGFIoS-rF8MXOIorBA"
)


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"👋Здравствуйте, {msg.from_user.first_name}\n"
                                             "Для определения вашего уникального камня в соответствии с натальной картой, введите вашу дату рождения в формате месяц.день\n"
                                             "Пример: 15.03", reply_markup=markups.menu_keyb
                           )


@dp.callback_query_handler(Text("start_process_birth_data"))
async def start_process_birth_data(call: types.CallbackQuery):
    await call.message.edit_text(text="Введите свою дату рождения", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Отмена", callback_data="back_to_menu")]
        ]
    ))
    await GetTextData.get_date_of_the_birth.set()


@dp.callback_query_handler(Text("back_to_menu"), state=GetTextData.get_date_of_the_birth)
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"Операция отменена, вы вернулись в главное меню", reply_markup=markups.menu_keyb)


@dp.callback_query_handler(Text("back_to_menu"))
async def back_to_menu(call: types.CallbackQuery):
    try:
        await call.message.edit_text(f"Вы вернулись в главное меню", reply_markup=markups.menu_keyb)
    except:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, f"Вы вернулись в главное меню", reply_markup=markups.menu_keyb)


@dp.callback_query_handler(Text("call_to_manager"))
async def call_to_manager(call: types.CallbackQuery):
    try:
        await call.message.edit_text("Напишите в профиль @Layda62",
                                     reply_markup=InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [InlineKeyboardButton("В главное меню", callback_data="back_to_menu")]
                                         ]
                                     ))
    except:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id,
                               f"Напишите в профиль @Layda62",
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [InlineKeyboardButton("В главное меню", callback_data="back_to_menu")]
                                   ]
                               ))


@dp.callback_query_handler(Text("watch_all_gems"))
async def watch_all_gems(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    keys = list(gem_photos.keys())
    await bot.send_photo(call.from_user.id, gem_photos[keys[0]][random.randint(0, len(keys[0]) - 1)],
                         caption=keys[0],
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Менеджер", callback_data="call_to_manager"),
                                     InlineKeyboardButton(text="Далее", callback_data="watch-next-1")
                                 ],
                                 [InlineKeyboardButton(text="В главное меню", callback_data="back_to_menu")]

                             ]
                         ))


@dp.callback_query_handler(Text(startswith="watch"))
async def get_next_item(call: types.CallbackQuery):
    act = call.data.split('-')[1]
    current_num = int(call.data.split('-')[2])
    new_current_num = current_num

    if not current_num >= len(gem_photos):
        new_current_num += 1 if act == 'next' else -1
    else:
        current_num = 0

    keys = list(gem_photos.keys())
    keyb = InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Менеджер", callback_data="call_to_manager"),
                                     InlineKeyboardButton(text="Далее", callback_data="watch-next-1")
                                 ],
                                 [InlineKeyboardButton(text="В главное меню", callback_data="back_to_menu")]

                             ]
                         )

    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_photo(call.from_user.id,
                         gem_nums_photos[current_num][random.randint(0, len(gem_nums_photos[current_num]) - 1)],
                         caption=keys[current_num],
                         reply_markup=keyb)


@dp.callback_query_handler(Text("job_examples"))
async def show_gem_examples(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, "Пожалуйста, подождите..")
    media = MediaGroup()
    [media.attach_video(video=open(f"resources/video/{i}.mp4", "rb")) for i in range(1, 10)]

    await bot.send_media_group(call.from_user.id, media=media)
    await bot.delete_message(call.from_user.id, call.message.message_id + 1)


@dp.message_handler(content_types=['text'], state=GetTextData.get_date_of_the_birth)
async def process_birth_data(msg: types.Message, state: FSMContext):
    try:
        text = msg.text
        day, month_t = text.split('.')

        if day.isnumeric() and month_t.isnumeric():
            month = numbers_months[month_t] if numbers_months.get(month_t) is not None else ""
            max_day = max_day_in_months_data[month] if max_day_in_months_data.get(month) is not None else ""

            if max_day != "":
                if 0 < int(day) <= max_day:
                    date = f"{int(day)}.{month_t}"
                    zodiac = [z for z in zodiacs if date in zodiacs[z]][0]

                    all_dekads = zodiacs_dates_data[zodiac]["dekads"]
                    dekad = [i for i in range(1, len(all_dekads) + 1) if date in all_dekads[i]][0]

                    answer = zodiacs_messages_data[zodiac]["dekads"][dekad]

                    media = MediaGroup()
                    photos = list(filter(lambda x: x.lower() in answer.lower(), gems))
                    await bot.send_message(msg.from_user.id, f"Вы - {zodiac}.\n"
                                                             f"Ваша декада - {dekad}\n\n"
                                                             f"{answer}", reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton("В главное меню", callback_data="back_to_menu")]
                        ]
                    ))
                    await state.finish()
                else:
                    await bot.send_message(msg.from_user.id, f"Вы некорректно ввели день\n"
                                                             f"День не может быть меньше или равен 0, а также больше, чем "
                                                             f"последний день месяца {month} - {max_day}",
                                           reply_markup=InlineKeyboardMarkup(
                                               inline_keyboard=[
                                                   [InlineKeyboardButton("Отмена", callback_data="back_to_menu")]
                                               ]
                                           ))
            else:
                await bot.send_message(msg.from_user.id, 'Вы некоректно ввели данные, пожалуйста, проверьте формат '
                                                         'сообщения: "месяц.день"', reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton("Отмена", callback_data="back_to_menu")]
                    ]
                ))
    except:
        await bot.send_message(msg.from_user.id, 'Вы некоректно ввели данные, пожалуйста, проверьте формат '
                                                 'сообщения: "месяц.день"', reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Отмена", callback_data="back_to_menu")]
            ]
        ))


@dp.message_handler(content_types=['photo', 'video'])
async def get_photo(msg: types.Message):
    try:
        photos = msg.photo
        print(f"\n\n'{photos[0].file_id}',")
    except:
        video = msg.video
        print(f"\n\n\n{video.file_id}")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
