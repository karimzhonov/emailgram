from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from storage import Session
from utils import Message, render_message as _


class EmailMessage(Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Answer', callback_data='email_message_answer')],
        [types.InlineKeyboardButton('Back', callback_data='back_to_email_message_list')],
    ])

    async def get_email_message(self):
        # Router
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]

        # Get Message
        client = self.data['email_client']
        uid = self.data['email_msg']
        messages = client.inbox(f'UID {uid}').__next__()
        await self.state.update_data(email_msg_full=messages)
        text = messages["text"]
        subject = messages["subject"]
        from_ = messages['from']
        date = messages['date']
        return _(etype, ename, eutil, subject,
                 subject=subject,
                 from_=from_,
                 date=date,
                 body=text)

    async def render(self):
        self.data = await self.get_data()
        text = await self.get_email_message()
        await self.call.message.edit_text(text)
        await self.call.message.edit_reply_markup(self.keyboard)


@dp.callback_query_handler(lambda c: c.data == 'back_to_email_message_list', state=Session.email_msg_util_name)
async def back_to_email_message_list(call: types.CallbackQuery, state: FSMContext):
    from views.users.inbox_message_list import InboxMessageList

    await Session.email_msg.set()
    await InboxMessageList(call, state).render()


@dp.callback_query_handler(lambda c: c.data == 'email_message_answer', state=Session.email_msg_util_name)
async def email_message_answer_func(call: types.CallbackQuery, state: FSMContext):
    from views.users.new_emial_message import NewEmailMessage

    data = await state.get_data()
    msg = data['email_msg_full']
    await state.update_data({
        'new_email_message_to_email': msg['from'],
        'new_email_message_subject': f'Re: {msg["subject"]}',
    })

    await Session.new_email_message_message.set()
    await NewEmailMessage(state).render_get_message()
