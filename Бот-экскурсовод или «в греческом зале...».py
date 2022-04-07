import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = 'token'


def enter_room(update, context):
    update.message.reply_text(
        "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!",
        reply_markup=ReplyKeyboardMarkup([['/first_room']], one_time_keyboard=True))
    return 1


def first_room(update, context):
    update.message.reply_text(
        f'В данном зале представлено: Искусство средневекового Азербайджана',
        reply_markup=ReplyKeyboardMarkup([['/second_room', '/exit_room']], one_time_keyboard=True))
    return 2


def second_room(update, context):
    update.message.reply_text(
        f'В данном зале представлено: Салтыковская лестница',
        reply_markup=ReplyKeyboardMarkup([['/third_room']], one_time_keyboard=True))
    return 3


def third_room(update, context):
    update.message.reply_text(
        f'В данном зале представлено: Портретная галерея дома Романовых',
        reply_markup=ReplyKeyboardMarkup([['/fought_room', '/first_room']], one_time_keyboard=True))
    return 4


def fought_room(update, context):
    update.message.reply_text(
        f'В данном зале представлено: Портреты русских императоров',
        reply_markup=ReplyKeyboardMarkup([['/first_room']], one_time_keyboard=True))
    return 1


def exit_room(update, context):
    update.message.reply_text(f'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!')
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('enter_room', enter_room)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [CommandHandler('first_room', first_room)],
            2: [CommandHandler('second_room', second_room), CommandHandler('exit_room', exit_room)],  # РАБОТАЕТ ТОЛЬКО ПРИ ТАКОМ ПОРЯДКЕ
            3: [CommandHandler('third_room', third_room)],
            4: [CommandHandler('fought_room', fought_room), CommandHandler('first_room', first_room)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('enter_room', enter_room))
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()