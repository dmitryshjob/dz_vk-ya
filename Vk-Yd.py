
import requests
import json
from tqdm import tqdm

#
# Ya_token1 = input('fff')
# print(Ya_token1[])

class VK:

    def __init__(self,version): # основные параметры запроса

        self.token = Vk_token
        self.id = '708834799'
        self.version = version
        self.json, self.export_dict = self.sort_info1()
        
        
    def sort_info1(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token' : Vk_token,
            'v' : '5.131',
            'album_id' : 'profile',
            'owner_id': VK_id,
            'extended': 1,
            'photo_sizes': 1}

        req = requests.get(url, params).json()['response']['items']
        
        repeat_likes = {}
        list_files = []
        file_name = {}
        for x in req:   
            max_sizes_photo = sorted(x['sizes'], key=lambda x: x['height'])[-1] 
            if x['likes']['count'] in repeat_likes:
                repeat_likes[x['likes']['count']] += 1                
            else:
                repeat_likes[x['likes']['count']] = 1        
            if repeat_likes.get(x['likes']['count']) > 1:
                max_sizes_photo['file_name'] = str(x['date']) + '.jpg'                      
            else:
                max_sizes_photo['file_name'] = str(x['likes']['count']) + '.jpg'                   
            list_files.append({'file_name':max_sizes_photo['file_name'],'size':max_sizes_photo['type']})    
            file_name.update({max_sizes_photo['file_name']:max_sizes_photo['url']})
            with open('VK_photo', 'w') as outfile:  # информация по фотографиям в файле VK_photo
                json.dump(list_files, outfile)         
        return  list_files, file_name  




class Yandex:

    host = 'https://cloud-api.yandex.net'
    def __init__(self, folder_name, Ya_token, num = 5): # основные параметры для загрузки фотографий
        self.token = Ya_token
        self.files_num = num
        self.url = f'{self.host}/v1/disk/resources/upload'
        self.headers = {'Authorization': self.token}
        self.folder = self._create_folder(folder_name)

    def _create_folder(self, folder_name): # создания папки
        url = f'{self.host}/v1/disk/resources'
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка <<<<< {folder_name} >>>>> успешно создана. \n')
        else:
            print(f'\nПапка <<<<< {folder_name} >>>> уже существует!!! \n') 
        return folder_name

    def getting_link(self, folder_name): # получения ссылки для загрузки фотографий
        url = f'{self.host}/v1/disk/resources'
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        file_repetition = []        
        for name in resource:
            file_repetition.append(name['name'])  
        return file_repetition

    def uploading_photos(self, dict_files): # загрузка фотографий

        files_in_folder = self.getting_link(self.folder)
        copy_counter = 0        
        for key, i in zip(dict_files.keys(), tqdm(range(self.files_num ))):           
            if copy_counter < self.files_num:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    copy_counter += 1
                else:
                    print(f' Файл {key} уже существует и не будет скопирован')
            else:
                break
        print(f'Новых файлов скопировано : {copy_counter}')
            


if __name__ == '__main__':

    version = '5.131'
    
    VK_id = ''
   

  
    Ya_token = ''
    Vk_token = 'vk1.a.RNDxYHKIjleAZ12t283z4aTV-uWsBfz49mAdxy41CuGEcBpsEiVMNjWIsrotc8PNtY05pJsYch0HB1osBDdFHaJ_BMBQvTqtuh0yTN34CW_GFn1-npzqvnpnFZfZ-rnAg-DTMSCpdtkhogbEhAMlanRpvsQYUt5hiWnVWTACJG70t7epvK4i2IktdsLkkAB2ho0A7Q53SPhTLo4B8DhF6A'
    
    VK = VK(Vk_token)  # Создаем экземпляр класса VK       
    yandex = Yandex('Photos from Vk', Ya_token) # Создаем экземпляр класса Yandex
    yandex.uploading_photos(VK.export_dict)  # Вызываем функцию для копирования фотографий        

