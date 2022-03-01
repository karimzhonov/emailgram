from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from bot import dp
from bot.storage import Session
from bot.client import Client
from bot.utils import Message, render_message as _

from config import ERROR_AUTH_TEXT

from database.models import Mail


class EmailAccountList(Message):

    async def get_emails_account_text(self):
        return _(f'{self.data["email_type"]}')

    async def get_emails_accounts_keyboard(self):
        mails = await Mail.get_mails(self.call.message.chat.id, email_type=self.data['email_type'], is_active=True)
        kb = types.InlineKeyboardMarkup()

        for mail in mails:
            callback_data = str(mail.email)
            kb.inline_keyboard.append([types.InlineKeyboardButton(callback_data, callback_data=callback_data)])

        # Add Account
        kb.inline_keyboard.append([types.InlineKeyboardButton('Add Email', callback_data=f'add_email')])
        kb.inline_keyboard.append([types.InlineKeyboardButton('Back', callback_data='back_to_email_type')])
        return kb

    async def render(self):
        self.data = await self.get_data()
        kb = await self.get_emails_accounts_keyboard()
        text = await self.get_emails_account_text()

        await self.call.message.edit_text(text)
        await self.call.message.edit_reply_markup(kb)


@dp.callback_query_handler(lambda c: c.data == 'back_to_email_type', state=Session.email_name)
async def back_to_email_type(call: types.CallbackQuery, state: FSMContext):
    from bot.views.start import start

    await Session.email_type.set()
    await start(call.message, state)

@dp.callback_query_handler(lambda c: c.data == 'add_email', state=Session.email_name)
async def add_email(call: types.CallbackQuery, state: FSMContext = None):
    from bot.views.users.add_email import add_mail_account

    await state.update_data(email_name='add_email')
    await add_mail_account(call, state)


@dp.callback_query_handler(state=Session.email_name)
async def open_mail(call: types.CallbackQuery, state: FSMContext):
    from bot.views.users.email_utils_list import EmailUtilsList

    email_name = call.data
    await state.update_data({
        'email_name': email_name,
    })
    data = await state.get_data()
    # Mail database
    mail = await Mail.get(user_id=data['user_id'], email=data['email_name'],
                          email_type=data['email_type'], is_active=True)
    # Mail Client
    email = Client(mail.email, mail.password, mail.email_type)
    if email.check_email() == 'OK':
        await Session.email_util_name.set()
        await state.update_data({
            'email_client': email,
        })
        await EmailUtilsList(call, state).render()
    else:
        await Session.email_util_name.set()
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton('Back', callback_data='back_to_emails_list')]
        ])

        text = _(data["email_type"],
                 body=ERROR_AUTH_TEXT)
        await call.message.edit_text(text, reply_markup=kb)
