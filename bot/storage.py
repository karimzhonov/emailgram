from aiogram.dispatcher.filters.state import State, StatesGroup


class Session(StatesGroup):
    user_id = State()
    email_type = State()
    email_name = State()
    email_util_name = State()
    email_msg = State()
    email_msg_util_name = State()

    start_idx = State()
    end_idx = State()
    email_msg_date = State()
    # Message id which editing
    callback_query_msg_id = State()
    # Add Email
    adding_email_name = State()
    adding_email_password = State()
    # Mail Client
    email_client = State()
    # Last msg data
    last_msg_text = State()
    last_msg_kb = State()




