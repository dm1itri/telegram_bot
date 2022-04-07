# Импортируем необходимые классы.
import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from random import randint
# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = 'token'

'''
# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    text = update.message.text
    update.message.reply_text(f'Я получил сообщение {update.message.text}')


def time(update, context):
    update.message.reply_text(datetime.now().strftime('%H:%M:%S'))


def date(update, context):
    update.message.reply_text(datetime.now().strftime('%d.%m.%y'))
'''


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='КУКУ!', reply_markup=timer_markup)
    return 3


def start(update, context):
    update.message.reply_text('Таймер или кубики', reply_markup=base_markup)
    return 1


def dice(update, context):
    update.message.reply_text('Какой кубик?', reply_markup=dice_markup)
    return 1


def dice_result(update, context):
    t = update.message.text
    reply_t = 'К сожалению, у меня нет таких кубиков'
    if t == '/6':
        reply_t = f'Выпало: {randint(1, 6)}'
    elif t == '/2x6':
        reply_t = f'Выпало: {randint(1, 6)} и {randint(1, 6)}'
    elif t == '/20':
        reply_t = f'Выпало: {randint(1, 20)}'
    update.message.reply_text(reply_t)


def timer(update, context):
    update.message.reply_text('На сколько установить таймер?', reply_markup=timer_markup)
    return 3


def timer_result(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    due = 0
    if update.message.text == '/30s':
        due = 30
    elif update.message.text == '/1m':
        due = 60
    elif update.message.text == '/5m':
        due = 300

    remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))

    reply_t = f'Вернусь через {due} секунд!'
    update.message.reply_text(reply_t, reply_markup=active_timer_markup)


def timer_close(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    reply_t = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    update.message.reply_text(reply_t, reply_markup=timer_markup)


def main():
    global base_markup, dice_markup, timer_markup, active_timer_markup
    base_keyboard = [['/dice', '/timer']]
    dice_keyboard = [['/6', '/2x6', '/20', '/stop']]
    timer_keyboard = [['/30s', '/1m', '/5m', '/stop']]
    close_keyboard = [['/close']]

    base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=True)
    dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
    timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
    active_timer_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=True)
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CommandHandler('dice', dice), CommandHandler('timer', timer)],
            3: [CommandHandler('timer', timer)],
        },
        fallbacks=[CommandHandler('stop', start)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("6", dice_result))
    dp.add_handler(CommandHandler("2x6", dice_result))
    dp.add_handler(CommandHandler("20", dice_result))

    dp.add_handler(CommandHandler("30s", timer_result, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("1m", timer_result, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("5m", timer_result, pass_job_queue=True, pass_chat_data=True))

    dp.add_handler(CommandHandler("close", timer_close))

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()