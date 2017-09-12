"""
Приложение-граббер фотографий из диалогов Вконтакте

"""

import vk
from auth import VKAuth
import config

def getDialogSel(url):
    url_params = url.split('?')[1:][0].split('&')
    for item in url_params:
        if item.split('=')[0] == 'sel':
            return item.split('=')[1] if item.split('=')[1][0] != 'c' else item.split('=')[1][1:]

Auth = VKAuth(['messages'], config.vk_app_id, '5.68')
Auth.auth()

access_token = Auth.get_token()
user_id = Auth.get_user_id()
