import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = ''


def start(update, context):
    update.message.reply_text("Я к вам пишу — чего же боле?")
    context.user_data['line_number'] = 2
    return 1


def user_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    with open('письмо_татьяны', 'r', encoding='utf-8') as f:
        n = context.user_data['line_number']
        t = f.read().split('\n')
        if t[n - 1] == update.message.text:
            if n >= 78:
                update.message.reply_text('Было приятно иметь с Вами дело!',
                                          reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            update.message.reply_text(t[n], reply_markup=ReplyKeyboardRemove())
            context.user_data['line_number'] += 2
            return 1
    if '/suphler' == update.message.text:
        update.message.reply_text(
            'Вы даже не пытались',
            reply_markup=ReplyKeyboardMarkup([['/suphler']], one_time_keyboard=True))
    else:
        update.message.reply_text(
            'нет, не так',
            reply_markup=ReplyKeyboardMarkup([['/suphler']], one_time_keyboard=True))
    return 2


def suphler(update, context):
    n = context.user_data['line_number']
    if n >= 78:
        update.message.reply_text('Было приятно иметь с Вами дело!')
        return ConversationHandler.END
    with open('письмо_татьяны', 'r', encoding='utf-8') as f:
        t = f.read().split('\n')[n - 1]
    update.message.reply_text(t, reply_markup=ReplyKeyboardRemove())
    context.user_data['line_number'] += 1


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
            2: [CommandHandler('suphler', suphler), MessageHandler(Filters.text, user_response)]
        },
        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()