from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PREMIUM_LINK


def get_start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Создать описание", callback_data="start_generation")],
        [InlineKeyboardButton(text="💎 Премиум", callback_data="premium_info")],
        [InlineKeyboardButton(text="🎁 Пригласить друга", callback_data="referral_info")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")],
    ])


def get_result_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Ещё", callback_data="restart"),
            InlineKeyboardButton(text="✏️ Изменить", callback_data="edit"),
        ],
    ])


def get_premium_kb(price: int, discount: int = 0):
    button_text = f"💎 Купить премиум за {price}₽"
    if discount:
        button_text += f" (-{discount}%)"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, url=PREMIUM_LINK)],
    ])


def get_referral_kb(referral_link: str, share_link: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить другу", url=share_link)],
        [InlineKeyboardButton(text="🔗 Открыть мою ссылку", url=referral_link)],
    ])
