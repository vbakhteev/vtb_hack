import os
import enum

from telegram import ForceReply, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
)


from src.api_client import ApiClient
from src.utils import reply_keyboard, inline_keyboard, get_match_regex


class ConversationStates(enum.Enum):
    asked_role = enum.auto()


USER_ROLES = [
    {
        "name": "Менеджер",
        "role": "manager",
    },
    {
        "name": "Бухгалтер",
        "role": "accountant",
    },
]


def main_menu(update: Update, context: CallbackContext):
    text = "Нажми 'Новость', чтобы получить новое сообщение"
    keyboard = reply_keyboard(
        buttons=[["Новость"]],
    )

    update.effective_user.send_message(
        text=text,
        reply_markup=keyboard,
    )

    return ConversationHandler.END


def start(update: Update, context: CallbackContext):
    user = update.effective_user

    text = "Выбери свою роль"
    keyboard = reply_keyboard(
        buttons=[[ur["name"]] for ur in USER_ROLES],
        one_time_keyboard=True,
    )
    user.send_message(
        text=text,
        reply_markup=keyboard,
    )

    return ConversationStates.asked_role


def register_user(update: Update, context: CallbackContext):
    user = update.effective_user

    role_name = update.message.text
    role = [ur["role"] for ur in USER_ROLES if ur["name"] == role_name][0]

    api_client.register(
        user_id=user.id,
        full_name=user.full_name,
        user_type=role,
    )

    return main_menu(update, context)


def get_publication(update: Update, context: CallbackContext):
    user = update.effective_user

    rec = api_client.recommend(user_id=user.id)
    title = rec["title"]
    summary = rec["summary"]
    publication_url = rec["url"]
    publication_id = rec["publication_id"]

    text = f"<b>{title}</b>\n<i>{summary}</i>"

    keyboard = inline_keyboard(
        buttons=[["👍", "👎"], [publication_url]],
        callbacks=[
            [f"like_{publication_id}", f"dislike_{publication_id}"],
            [f"url_{publication_id}"],
        ],
    )

    user.send_message(
        text=text,
        reply_markup=keyboard,
        parse_mode='HTML',
    )


def receive_feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data.split('_')
    feedback = data[0]
    publication_id = int(data[1])
    user_id = update.effective_user.id

    api_client.save_event(
        user_id=user_id,
        publication_id=publication_id,
        event_type=feedback,
    )
    publication_url = api_client.get_publication_url(
        publication_id=publication_id,
    )

    keyboard = inline_keyboard(
        buttons=[[publication_url]],
        callbacks=[[f"url_{publication_id}"]],
    )

    query.edit_message_reply_markup(
        reply_markup=keyboard,
    )


# def click(update: Update, context: CallbackContext):
#     query = update.callback_query
#     query.answer()

#     publication_id = int(query.data.split('_')[1])
#     user_id = update.effective_user.id

#     api_client.save_event(
#         user_id=user_id,
#         publication_id=publication_id,
#         event_type='click',
#     )


def add_handlers(updater):
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            ConversationStates.asked_role: [
                MessageHandler(get_match_regex(*[ur["name"] for ur in USER_ROLES]), register_user),
                MessageHandler(Filters.all, start),
            ],
        },
        fallbacks=[MessageHandler(Filters.all, main_menu),]
    )

    handlers = [
        conv_handler,
        MessageHandler(get_match_regex('Новость'), get_publication),
        CallbackQueryHandler(receive_feedback, pattern=f'^(dis)?like_'),
        MessageHandler(Filters.text, main_menu),
    ]

    for handler in handlers:
        dispatcher.add_handler(handler)


def main(token):
    updater = Updater(token)
    add_handlers(updater)
    updater.start_polling(drop_pending_updates=True)
    updater.idle()


if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")

    api_client = ApiClient(
        host=os.getenv("API_URL"),
    )

    main(token=token)
