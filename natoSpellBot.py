from dotenv import dotenv_values
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
import logging


def load_nato_dictionary():
    pass


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I am a spellBot. I can spell your text "
        "using the Nato Alphabet. Use \\spell followed by your text "
        "to ask me to spell.",
    )


def source_data():
    # TODO: Source data from updatable repository/possibly API?
    data = {}
    with open("acronyms.csv", "r") as f:
        lines = f.readlines()
    for line in lines:
        entries = line.split(",")
        if len(entries) != 2:
            pass
        else:
            data[entries[0].upper()] = entries[1]
    return data


def generate_response(context):
    if len(context.args) != 1:
        return "Please specify a single acronym."

    acronym = context.args[0]

    data = source_data()

    try:
        return f"{acronym} stands for {data[acronym.upper()]}"
    except KeyError:
        return (
            f"Sorry, I don't understand this acronym neither. "
            f"Maybe try <a href='https://www.google.com/search?q={acronym}'>here</a>?"
        )


def query(update, context):
    response = generate_response(context)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.HTML
    )


def run_bot():
    token = dotenv_values()["token"]

    updater = Updater(token=token, use_context=True)
    # define shortcut to dispatcher
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    query_handler = CommandHandler("q", query)
    dispatcher.add_handler(query_handler)

    updater.start_polling()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    run_bot()
