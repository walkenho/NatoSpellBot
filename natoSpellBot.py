import json
import logging
import os
import pathlib

from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

DATAPATH = pathlib.Path(__file__).parent / "data"
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = os.environ.get("TOKEN")


def load_nato_dictionary():
    with open(DATAPATH / "natoalphabet.json", "r") as f:
        return json.load(f)


def nato_spell(tokenlist):
    nato_dict = load_nato_dictionary()
    return (
        " ".join(tokenlist)
        + ":\n"
        + "\n".join(
            [
                word + " - " + " ".join([nato_dict[letter.upper()] if letter.isalpha() else letter for letter in word])
                for word in tokenlist
            ]
        )
    )


def generate_response(update, context):
    logging.info("Generating Response")
    response = nato_spell(context.args)
    # TODO: convert this into something that can be used to spell somebody's full name and user name
    # print(update.effective_user)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.HTML
    )


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I am NatoSpellBot, I have international spelling power! I can spell your text "
        "using the Nato Alphabet. Use /spell followed by your text to tell me what to spell.",
    )


def run_bot():

    updater = Updater(token=TOKEN, use_context=True)
    # define shortcut to dispatcher
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    query_handler = CommandHandler("spell", generate_response)
    dispatcher.add_handler(query_handler)

    logging.info(f"PORT: {PORT}")
    updater.start_polling()
    #updater.start_webhook(listen="0.0.0.0",
    #                      port=int(PORT),
    #                      url_path=TOKEN,
    #                      webhook_url='https://nato-spellbot.herokuapp.com/' + TOKEN)
    logging.info("I am running")
    #updater.idle()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    run_bot()
