from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from urllib.parse import quote

from states import SeoStates
from keyboards import get_start_kb, get_result_kb, get_premium_kb, get_referral_kb
from database import (
    get_or_create_user,
    get_referral_count,
    increment_requests,
    check_premium_expired,
    register_user,
)
from ai_service import generate_description
from config import (
    FREE_LIMIT,
    MAX_REFERRALS,
    PREMIUM_PRICE,
    REFERRAL_DISCOUNT_PERCENT,
)

router = Router()


def get_premium_offer(user_id: int) -> tuple[int, int, int]:
    referral_count = min(get_referral_count(user_id), MAX_REFERRALS)
    discount = referral_count * REFERRAL_DISCOUNT_PERCENT
    discounted_price = PREMIUM_PRICE * (100 - discount) // 100
    return referral_count, discount, discounted_price


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()
    referrer_id = None
    if command.args and command.args.startswith("ref_"):
        try:
            referrer_id = int(command.args.removeprefix("ref_"))
        except ValueError:
            pass

    user, credited_referrer = register_user(
        message.from_user.id,
        message.from_user.username,
        referrer_id,
        MAX_REFERRALS,
    )
    check_premium_expired(message.from_user.id)
    user = get_or_create_user(message.from_user.id, message.from_user.username)

    if credited_referrer:
        count = get_referral_count(credited_referrer)
        discount = count * REFERRAL_DISCOUNT_PERCENT
        try:
            await message.bot.send_message(
                credited_referrer,
                f"🎉 По вашей ссылке пришёл новый пользователь!\n\n"
                f"Ваша скидка на премиум теперь {discount}% "
                f"({count} из {MAX_REFERRALS} друзей).",
            )
        except Exception:
            pass
    
    limit_text = "∞" if user["is_premium"] else str(FREE_LIMIT)
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Я помогу составить продающее SEO-описание для маркетплейсов.\n\n"
        f"📊 Использовано: {user['requests_count']} из {limit_text} запросов.\n\n"
        f"Нажми кнопку ниже, чтобы начать ✨",
        reply_markup=get_start_kb()
    )


@router.message(Command("help"))
@router.callback_query(F.data == "help")
async def cmd_help(obj):
    text = (
        "🆘 <b>Как пользоваться ботом:</b>\n\n"
        "1️⃣ Нажми «Создать описание»\n"
        "2️⃣ Введи название товара\n"
        "3️⃣ Укажи характеристики\n"
        "4️⃣ Добавь ключевые слова\n"
        "5️⃣ Получи готовое SEO-описание!\n\n"
        "📌 Команды:\n"
        "/start — начать заново\n"
        "/help — эта справка\n"
        "/balance — проверить баланс\n"
        "/premium — информация о подписке\n"
        "/referral — пригласить друзей и получить скидку\n"
        "/cancel — отменить ввод"
    )
    if isinstance(obj, CallbackQuery):
        await obj.message.answer(text, parse_mode="HTML")
        await obj.answer()
    else:
        await obj.answer(text, parse_mode="HTML")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_start_kb())


@router.message(Command("balance"))
async def cmd_balance(message: Message):
    check_premium_expired(message.from_user.id)
    user = get_or_create_user(message.from_user.id, message.from_user.username)
    
    if user["is_premium"]:
        until_text = user['premium_until'][:10] if user['premium_until'] else 'N/A'
        await message.answer(
            f"💎 <b>Премиум активен</b>\n\n"
            f"📊 Запросов использовано: {user['requests_count']}\n"
            f"⚡ Лимит: ∞ (безлимит)\n"
            f"📅 Действует до: {until_text}",
            parse_mode="HTML"
        )
    else:
        remaining = max(0, FREE_LIMIT - user["requests_count"])
        await message.answer(
            f"📊 <b>Ваш баланс</b>\n\n"
            f"✅ Использовано: {user['requests_count']} из {FREE_LIMIT}\n"
            f"🎁 Осталось бесплатных: {remaining}\n\n"
            f"💎 Купите премиум для безлимита → /premium",
            parse_mode="HTML"
        )


@router.message(Command("premium"))
@router.callback_query(F.data == "premium_info")
async def cmd_premium(obj):
    user_id = obj.from_user.id
    get_or_create_user(user_id, obj.from_user.username)
    _, discount, discounted_price = get_premium_offer(user_id)
    text = (
        "💎 <b>Премиум-подписка</b>\n\n"
        "✅ Безлимитные генерации\n"
        "✅ Приоритетная обработка\n"
        "✅ Расширенные промпты\n\n"
        f"🔥 Стоимость: {discounted_price}₽/мес"
        + (f" вместо {PREMIUM_PRICE}₽ (скидка {discount}%)\n" if discount else "\n")
        + "Для оплаты напишите администратору 👇"
    )
    keyboard = get_premium_kb(discounted_price, discount)
    if isinstance(obj, CallbackQuery):
        await obj.message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(Command("referral"))
@router.callback_query(F.data == "referral_info")
async def cmd_referral(obj):
    user_id = obj.from_user.id
    get_or_create_user(user_id, obj.from_user.username)
    referral_count, discount, _ = get_premium_offer(user_id)
    bot_info = await obj.bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    share_text = (
        "Попробуй этого Telegram-бота для создания SEO-описаний товаров!"
    )
    share_link = (
        f"https://t.me/share/url?url={quote(referral_link, safe='')}"
        f"&text={quote(share_text, safe='')}"
    )
    text = (
        "🎁 <b>Реферальная программа</b>\n\n"
        f"Приглашайте друзей и получайте скидку {REFERRAL_DISCOUNT_PERCENT}% "
        f"за каждого нового пользователя. Максимальная скидка — "
        f"{MAX_REFERRALS * REFERRAL_DISCOUNT_PERCENT}%.\n\n"
        f"👥 Приглашено: {referral_count} из {MAX_REFERRALS}\n"
        f"🏷 Ваша скидка: {discount}%\n\n"
        f"Ваша ссылка:\n<code>{referral_link}</code>"
    )
    keyboard = get_referral_kb(referral_link, share_link)
    if isinstance(obj, CallbackQuery):
        await obj.message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data == "start_generation")
async def start_generation(callback: CallbackQuery, state: FSMContext):
    check_premium_expired(callback.from_user.id)
    user = get_or_create_user(callback.from_user.id, callback.from_user.username)
    
    if not user["is_premium"] and user["requests_count"] >= FREE_LIMIT:
        _, discount, discounted_price = get_premium_offer(callback.from_user.id)
        await callback.message.answer(
            "⛔ Лимит бесплатных запросов исчерпан!\n\n"
            "Купи премиум и продолжай без ограничений 💎",
            reply_markup=get_premium_kb(discounted_price, discount)
        )
        await callback.answer()
        return

    await state.set_state(SeoStates.waiting_name)
    await callback.message.answer("📝 <b>Шаг 1/3.</b> Введи название товара:", parse_mode="HTML")
    await callback.answer()


@router.message(SeoStates.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(SeoStates.waiting_specs)
    await message.answer(
        "✅ Принял!\n\n"
        "📋 <b>Шаг 2/3.</b> Опиши характеристики товара "
        "(материал, размер, цвет, особенности):",
        parse_mode="HTML"
    )


@router.message(SeoStates.waiting_specs)
async def process_specs(message: Message, state: FSMContext):
    await state.update_data(specs=message.text.strip())
    await state.set_state(SeoStates.waiting_keywords)
    await message.answer(
        "✅ Отлично!\n\n"
        "🔑 <b>Шаг 3/3.</b> Введи ключевые слова через запятую "
        "(например: платье, летнее, для офиса, хлопок):",
        parse_mode="HTML"
    )


@router.message(SeoStates.waiting_keywords)
async def process_keywords(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text.strip())
    data = await state.get_data()

    loading_msg = await message.answer("🤖 Генерирую описание... подожди пару секунд ✨")
    result = generate_description(data["name"], data["specs"], data["keywords"])

    try:
        await loading_msg.delete()
    except Exception:
        pass

    await message.answer(
        f"🎉 <b>Готово!</b>\n\n{result}",
        parse_mode="HTML",
        reply_markup=get_result_kb()
    )

    increment_requests(message.from_user.id)
    await state.clear()


@router.callback_query(F.data == "restart")
async def restart(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    check_premium_expired(callback.from_user.id)
    user = get_or_create_user(callback.from_user.id, callback.from_user.username)
    
    if not user["is_premium"] and user["requests_count"] >= FREE_LIMIT:
        _, discount, discounted_price = get_premium_offer(callback.from_user.id)
        await callback.message.answer(
            "⛔ Лимит исчерпан! Купи премиум 💎",
            reply_markup=get_premium_kb(discounted_price, discount)
        )
        await callback.answer()
        return

    await state.set_state(SeoStates.waiting_name)
    await callback.message.answer("📝 <b>Шаг 1/3.</b> Введи название товара:", parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "edit")
async def edit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(SeoStates.waiting_name)
    await callback.message.answer(
        "✏️ Начинаем сначала.\n\n"
        "📝 <b>Шаг 1/3.</b> Введи название товара:",
        parse_mode="HTML"
    )
    await callback.answer()
