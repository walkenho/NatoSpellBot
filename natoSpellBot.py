import json

from dotenv import dotenv_values
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
import logging

import pathlib
DATAPATH = pathlib.Path(__file__).parent/'data'


def load_nato_dictionary():
    with open(DATAPATH/'natoalphabet.json', 'r') as f:
        return json.load(f)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I am NatoSpellBot, I have international spelling power! I can spell your text "
        "using the Nato Alphabet. Use /spell followed by your text to tell me what to spell."
    )


def nato_spell(tokenlist):
    nato_dict = load_nato_dictionary()
    return (
            ' '.join(tokenlist)
            + ':\n'
            + '\n'.join([word + ' - ' + " ".join([nato_dict[letter] for letter in word.upper()]) for word in tokenlist])
    )


def generate_response(update, context):
    response = nato_spell(context.args)
    print(update.chat_member)
    print(update.effective_user)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.HTML
    )


def run_bot():
    token = dotenv_values('.env')["TOKEN"]

    updater = Updater(token=token, use_context=True)
    # define shortcut to dispatcher
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    query_handler = CommandHandler("spell", generate_response)
    dispatcher.add_handler(query_handler)

    updater.start_polling()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    run_bot()
