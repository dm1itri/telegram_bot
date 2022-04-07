import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from json import load
from random import choice

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = ''


def start(update, context):
    # update.message.reply_text("Предлагаю пройти опрос")
    with open('тестирующая_система.json') as f:
        f = load(f)
    d_first = choice(f['test'])
    f['test'].remove(d_first)
    context.user_data['questions'] = f['test']
    context.user_data['response'] = d_first['response']
    context.user_data['corr_response'] = 0
    update.message.reply_text(d_first['question'])
    return 1


def user_response(update, context):
    if not context.user_data['questions']:
        update.message.reply_text(f'Ваш результат: {context.user_data["corr_response"]}\n'
                                  f'Чтобы попробовать ещё раз введите /start')
        return ConversationHandler.END
    if update.message.text.lower() == context.user_data['response'].lower():
        context.user_data['corr_response'] += 1
    t = choice(context.user_data['questions'])
    context.user_data['questions'].remove(t)
    context.user_data['response'] = t['response']
    update.message.reply_text(t['question'])
    return 1


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, user_response)],
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    # dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()