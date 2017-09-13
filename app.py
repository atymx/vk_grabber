"""
Приложение-граббер фотографий из диалогов Вконтакте

"""

import vk
import config
import time
import webbrowser
import os
from urllib.request import urlretrieve


def getDialogSel(url):
    url_params = url.split('?')[1:][0].split('&')
    for item in url_params:
        if item.split('=')[0] == 'sel':
            return item.split('=')[1] if item.split('=')[1][0] != 'c' else 2000000000 + int(item.split('=')[1][1:])


print('Сейчас сейчас откроется браузер. Дайте приложению доступы, скопируйте токен и вернитесь в консоль')
time.sleep(1)
webbrowser.open('https://oauth.vk.com/authorize?client_id={}&scope=photos,audio,video,docs,notes,pages,status,offers,'
                'questions,wall,groups,messages,email,notifications,stats,ads,offline,docs,pages,stats,'
                'notifications&response_type=token'.format(config.vk_app_id))

print('Вставьте токен. Для вас это безопасно!')
access_token = input()

session = vk.Session(access_token=access_token)
api = vk.API(session)

print('Спасибо, теперь скопируйте ссылку на диалог/беседу')
sel = getDialogSel(input())

# Через API Вконтакте получаем вложения(фотографии)
data = api.messages.getHistoryAttachments(peer_id=sel, media_type='photo', count=200)

# Сохраняем  массив url'ы всех фотографий
pictures = []
for i in range(1, len(data) - 1):
    pictures.append(data[str(i)]['photo']['src_big'])

# Создаем папку, в которую будем скачивать изображения
if not os.path.exists('pictures'):
    os.mkdir('pictures')

count = 0
errors = 0
for url in pictures:
    count += 1
    print('Загрузка фотографии {}/{}'.format(count, len(pictures)))
    print(url)
    try:
        urlretrieve(url, 'pictures/img{}.jpg'.format(count))
    except Exception:
        print('Не удалось загрузить изображение №{}'.format(count))
        errors += 1
    else:
        print('Изображение №{} успешно загружено'.format(count))

print('Загрузка завершена!')
print('Количество ошибок - {}'.format(errors))
