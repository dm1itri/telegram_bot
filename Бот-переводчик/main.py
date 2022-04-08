import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from googletrans import Translator

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = ''


def echo(update, context):
    if context.user_data.get('input_lang', False):
        lang = context.user_data['input_lang']
        translator = Translator()
        t = translator.translate(update.message.text, src=lang, dest='ru' if lang == 'en' else 'en')
        update.message.reply_text(t.text)
    else:
        update.message.reply_text('Выберите язык ввода',
                                  reply_markup=ReplyKeyboardMarkup([['/en', '/ru']],
                                                                   one_time_keyboard=False))


def england_lang(update, context):
    context.user_data['input_lang'] = 'en'
    update.message.reply_text('Язык ввода сменен на английский',
                              reply_markup=ReplyKeyboardMarkup([['/ru']],
                                                               one_time_keyboard=False))


def russian_lang(update, context):
    context.user_data['input_lang'] = 'ru'
    update.message.reply_text('Язык ввода сменен на русский',
                              reply_markup=ReplyKeyboardMarkup([['/en']],
                                                               one_time_keyboard=False))


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('en', england_lang))
    dp.add_handler(CommandHandler('ru', russian_lang))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()