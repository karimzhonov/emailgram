from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from storage import Session
from utils import Message, render_message as _


class InboxMessageList(Message):
    async def get_email_message_list_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        return _(f'{etype}', f'{ename}', f'{eutil}')

    async def get_email_message_list_keyboard(self):
        kb = types.InlineKeyboardMarkup()
        client_inbox = self.data['email_client']

        counter = 0
        max_count = 10
        for m in client_inbox.inbox():
            if counter >= max_count:
                await self.update_data(email_msg_date=m["date"])
                break
            counter += 1
            title = f'{m["subject"]}'
            callback_data = f'{m["uid"]}'
            kb.inline_keyboard.append([types.InlineKeyboardButton(title, callback_data=callback_data)])

        await self.update_data(email_client=client_inbox)
        kb.inline_keyboard.append([types.InlineKeyboardButton('<<', callback_data='email_message_list_previus'),
                                   types.InlineKeyboardButton('>>', callback_data='email_message_list_next')])

        kb.inline_keyboard.append([types.InlineKeyboardButton('Back', callback_data='back_to_email_utils_list')])
        return kb

    async def render(self):
        self.data = await self.get_data()
        text = await self.get_email_message_list_text()
        kb = await self.get_email_message_list_keyboard()
        await self.call.message.edit_text(text)
        await self.call.message.edit_reply_markup(kb)
        return text, kb


@dp.callback_query_handler(lambda c: c.data == 'email_message_list_next', state=Session.email_msg)
async def email_message_list_next(call: types.CallbackQuery, state: FSMContext):
    await Session.email_msg.set()
    await InboxMessageList(call, state).render()



@dp.callback_query_handler(lambda c: c.data == 'back_to_email_utils_list', state=Session.email_msg)
async def back_to_email_utils_list(call: types.CallbackQuery, state: FSMContext):
    from views.users.email_utils_list import EmailUtilsList

    await Session.email_util_name.set()
    await EmailUtilsList(call, state).render()



@dp.callback_query_handler(state=Session.email_msg)
async def open_message(call: types.CallbackQuery, state: FSMContext):
    from views.users.message import EmailMessage

    await Session.email_msg_util_name.set()
    await state.update_data({
        'email_msg': call.data
    })

    await EmailMessage(call, state).render()

