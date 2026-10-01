import os
import sys
import tempfile


def test_env():
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("BOT_TOKEN")
    if not token or token == "ваш_токен_от_BotFather":
        print("❌ BOT_TOKEN не настроен в .env")
        return False
    
    print("✅ BOT_TOKEN настроен")
    return True


def test_imports():
    try:
        import config
        import database
        import ai_service
        import states
        import keyboards
        import handlers
        print("✅ Все модули импортируются")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


def test_database():
    original_db_path = None
    try:
        import database
        original_db_path = database.DB_PATH
        with tempfile.TemporaryDirectory() as temp_dir:
            database.DB_PATH = os.path.join(temp_dir, "test.db")
            database.init_db()

            user = database.get_or_create_user(999999, "test_user")
            assert user["id"] == 999999
            assert user["requests_count"] == 0

            database.increment_requests(999999)
            user = database.get_or_create_user(999999, "test_user")
            assert user["requests_count"] == 1

            referrer_id = 999990
            database.get_or_create_user(referrer_id, "referrer")
            for user_id in range(999991, 999995):
                _, credited_referrer = database.register_user(
                    user_id, f"referred_{user_id}", referrer_id, 3
                )
                if user_id < 999994:
                    assert credited_referrer == referrer_id
                else:
                    assert credited_referrer is None
            assert database.get_referral_count(referrer_id) == 3

            _, credited_again = database.register_user(
                999991, "referred_again", referrer_id, 3
            )
            assert credited_again is None

            _, self_referral = database.register_user(
                999989, "self_referral", 999989, 3
            )
            assert self_referral is None

            _, missing_referrer = database.register_user(
                999988, "missing_referrer", 123456, 3
            )
            assert missing_referrer is None
        
        print("✅ База данных работает")
        return True
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")
        return False
    finally:
        if original_db_path is not None:
            database.DB_PATH = original_db_path


def test_ai_fallback():
    try:
        import ai_service
        result = ai_service.generate_description("Тест", "тест", "тест")
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Тест" in result
        
        print("✅ AI-заглушка работает")
        return True
    except Exception as e:
        print(f"❌ Ошибка AI: {e}")
        return False


def test_keyboards():
    try:
        import keyboards
        
        kb1 = keyboards.get_start_kb()
        assert kb1 is not None
        
        kb2 = keyboards.get_result_kb()
        assert kb2 is not None
        
        kb3 = keyboards.get_premium_kb(693, 30)
        assert kb3 is not None
        assert "693₽" in kb3.inline_keyboard[0][0].text
        assert "-30%" in kb3.inline_keyboard[0][0].text

        kb4 = keyboards.get_referral_kb(
            "https://t.me/test_bot?start=ref_1",
            "https://t.me/share/url?url=test",
        )
        assert kb4 is not None
        
        print("✅ Клавиатуры работают")
        return True
    except Exception as e:
        print(f"❌ Ошибка клавиатур: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Запуск автоматических тестов...\n")
    
    results = [
        test_env(),
        test_imports(),
        test_database(),
        test_ai_fallback(),
        test_keyboards(),
    ]
    
    print("\n" + "="*50)
    if all(results):
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        print("\nЗапустите: python bot.py")
        sys.exit(0)
    else:
        print("💥 Есть проблемы. Исправьте их перед запуском.")
        sys.exit(1)
