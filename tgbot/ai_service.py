import logging
from config import AI_API_KEY, AI_BASE_URL, AI_MODEL


def generate_description(name: str, specs: str, keywords: str) -> str:
    if not AI_API_KEY:
        return (
            f"🛍 {name}\n\n"
            f"✨ {specs}\n\n"
            f"🔑 Ключевые слова: {keywords}\n\n"
            f"💡 [AI-ключ не настроен]\n\n"
            f"🛒 Закажите прямо сейчас!"
        )

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL if AI_BASE_URL else None
        )
        response = client.chat.completions.create(
            model=AI_MODEL if AI_MODEL else "gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": (
                    f"Ты SEO-копирайтер для маркетплейсов. "
                    f"Создай продающее описание товара.\n\n"
                    f"Название: {name}\n"
                    f"Характеристики: {specs}\n"
                    f"Ключевые слова: {keywords}\n\n"
                    f"Требования: эмодзи, абзацы, призыв к действию, 150-250 слов."
                )
            }],
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"AI error: {e}")
        return "⚠️ Ошибка при генерации. Попробуйте позже."