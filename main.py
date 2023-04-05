
import time
from datetime import datetime
import requests
from pprint import pprint
class Vk:
    URL = 'https://api.vk.com/method/photos.get'
    dict_with_photos = {}
    def __init__(self,token):
        self.token = token
        self.params = {'access_token': self.token,
                  'v': '5.131',
                  'album_id': 'profile',
                  'photo_sies': '1',
                  'extended': '1'
                  }

    def get_photos(self):
        res = requests.get(Vk.URL, params=self.params)
        res = res.json()

        for i in res['response']['items']:
                date_of_photo = i['date']
                date_time = datetime.fromtimestamp(date_of_photo).strftime('%Y-%m-%d')
                name_of_photo = str(i['likes']['count']) + date_time

                index_photo = len(i['sizes'])
                url_photo = i['sizes'][index_photo - 1]['url']
                type_photo = i['sizes'][index_photo - 1]['type']
                Vk.dict_with_photos[name_of_photo] = url_photo, type_photo
        print(f'В словарь помещено {len(Vk.dict_with_photos.keys())} фотографий')

        return Vk.dict_with_photos

class YaDisk:
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    def __init__(self, ya_token):
        self.token = ya_token
        self.headers = {'Authorization': f'OAuth {self.token}'}
    def post_photos(self):
        for name_of_photo, url_photo in Vk.dict_with_photos.items():
            params = {'path': f'/vk_photo/{name_of_photo}', 'overwrite': 'true'}
            response = requests.get(YaDisk.URL, headers=self.headers, params=params)
            upload_url = response.json()['href']
            response = requests.put(upload_url, headers=self.headers, data=requests.get(url_photo[0]).content)
            if response.status_code == 201:
                print('Фотография успешно загружена на Яндекс.Диск')
            else:
                print('Ошибка загрузки фотографии на Яндекс.Диск')

if __name__ == "__main__":
    with open('TOKEN.txt', 'r') as file_object:
        token = file_object.read().strip()
    with open('TOKEN_Ya.txt', 'r') as file_object_1:
        ya_token = file_object_1.read().strip()

    Vk = Vk(token)
    YaDisk = YaDisk(ya_token)
    Vk.get_photos()
    YaDisk.post_photos()
