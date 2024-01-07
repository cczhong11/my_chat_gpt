import json


import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from Assistant.assistant import Assistant


config = json.load(open("config.json"))
my_assistant = Assistant("aws", config)


def is_allowed(update: Update) -> bool:
    """Check if the user is sane."""
    if update.effective_user.username not in ["cczhong", "tanyz33"]:
        update.message.reply_text(
            "You are not allowed to use this bot. Contact @cczhong to get access."
        )
        return False
    return True


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    try:
        user_input = update.message.text
        reply_msg = my_assistant.reply(user_input)
        if reply_msg is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Please try later"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=reply_msg
            )
    except KeyboardInterrupt:
        print(f">> Exiting...")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a tc bot"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.get("token")).build()
    reply_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), reply)
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(reply_handler)
    application.run_polling()
