from aiogram.fsm.state import State, StatesGroup


class ProgramCreate(StatesGroup):
    enter_name = State()
    enter_niche_description = State()
    enter_chats = State()
    confirm_settings = State()

class Auth(StatesGroup):
    enter_code = State()
    enter_password = State()
