from pychatgpt import Chat

import json


import traceback
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
        
# Initializing the chat class will automatically log you in, check access_tokens
chat = Chat(email="", password="") 




def is_allowed(update: Update) -> bool:
    """Check if the user is sane."""
    if update.effective_user.username not in ['cczhong']:
        update.message.reply_text(
            "You are not allowed to use this bot. Contact @Klingefjord to get access."
        )
        return False
    return True


def reply(update: Update, context: CallbackContext) -> None:
    """Call the OpenAI API."""

    if not is_allowed(update):
        return
    try:

        user_input = update.message.text
        answer = chat.ask(user_input)
        if answer is None:
            update.message.reply_text("Please try later")
        else:
            
            update.message.reply_text(answer)
    except KeyboardInterrupt:
        print(f">> Exiting...")



def main() -> None:
    """Start the bot."""
   
    updater = Updater()

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram


    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()






