# import time
# from datetime import datetime
# import requests
# from pprint import pprint
# with open('TOKEN.txt', 'r') as file_object:
#     token_VK = file_object.read().strip()
# with open('TOKEN_Ya.txt', 'r') as file_object_1:
#     token_YA = file_object_1.read().strip()
#
# URL = 'https://api.vk.com/method/photos.get'
# params = {'access_token': token_VK,
#           'v':'5.131',
#           'album_id': 'profile',
#           'photo_sies': '1',
#           'extended': '1'
#           }
# res = requests.get(URL, params=params)
# res = res.json()
# dict_with_photos = {}
#
# for i in res['response']['items']:
#     date_of_photo = i['date']
#     date_time = datetime.fromtimestamp(date_of_photo).strftime('%Y-%m-%d')
#     name_of_photo = str(i['likes']['count']) + date_time
#
#     index_photo = len(i['sizes'])
#     url_photo = i['sizes'][index_photo - 1]['url']
#     type_photo = i['sizes'][index_photo - 1]['type']
#     dict_with_photos[name_of_photo] = url_photo, type_photo
#     url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
#     headers = {'Authorization': f'OAuth {token_YA}'}
#     params = {'path': f'/vk_photo/{name_of_photo}', 'overwrite': 'true'}
#     response = requests.get(url, headers=headers, params=params)
#     upload_url = response.json()['href']
#     response = requests.put(upload_url, headers=headers, data=requests.get(url_photo).content)
#     if response.status_code == 201:
#         print('Фотография успешно загружена на Яндекс.Диск')
#     else:
#         print('Ошибка загрузки фотографии на Яндекс.Диск')
import requests
import time
from datetime import datetime
class VK:
    def _init_(self, token):
        self.token = token

    def get_photos(self):
        URL = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.token,
              'v':'5.131',
              'album_id': 'profile',
              'photo_sies': '1',
              'extended': '1'
              }

        res = requests.get(URL, params=params)
        res = res.json()
        dict_with_photos = {}

        for i in res['response']['items']:
            date_of_photo = i['date']
            date_time = datetime.fromtimestamp(date_of_photo).strftime('%Y-%m-%d')
            name_of_photo = str(i['likes']['count']) + date_time

            index_photo = len(i['sizes'])
            url_photo = i['sizes'][index_photo - 1]['url']
            type_photo = i['sizes'][index_photo - 1]['type']
            dict_with_photos[name_of_photo] = url_photo, type_photo

        return dict_with_photos

if __name__ == "__main__":
    with open('TOKEN.txt', 'r') as file_object:
        token = file_object.read().strip()
    print(token)
Vk_photos = VK(token)
dict_with_photos = Vk_photos.get_photos()
print(dict_with_photos)