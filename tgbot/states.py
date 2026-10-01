from aiogram.fsm.state import State, StatesGroup


class SeoStates(StatesGroup):
    waiting_name = State()
    waiting_specs = State()
    waiting_keywords = State()