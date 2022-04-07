from requests import get
import logging
from telegram.ext import Updater, MessageHandler, Filters

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def get_geocoder(geocode):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={geocode}&format=json"

    # Выполняем запрос.
    try:
        response = get(geocoder_request)
        json_response = response.json()
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        coords = toponym["Point"]["pos"]
        return coords, toponym_address
    except Exception:
        return False, False


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = 'token'


def echo(update, context):
    coords, address = get_geocoder(update.message.text)  # улица Доблести 24
    if coords:
        response = get("http://static-maps.yandex.ru/1.x/", params={'ll': ','.join(coords.split()),
                                                                    'l': 'sat',
                                                                    'pt': ','.join(coords.split())})
        context.bot.send_photo(update.message.chat_id, response.content, caption=address)
    else:
        update.message.reply_text('Данный адрес не найден')


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()