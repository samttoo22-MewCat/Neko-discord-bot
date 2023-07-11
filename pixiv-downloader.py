import requests 
import codecs 
import os 
from time import sleep 
 
class Pixiv: 
    def __init__(self): 
        self.requests = requests.Session() 
        self.headers = self.gen_new_headers() 
         
    def __headers(self): 
        headers = { 
            'Host': 'www.pixiv.net', 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3', 
            'Accept-Encoding': 'gzip, deflate', 
            'Referer': 'https://accounts.pixiv.net/' 
        } 
        return headers 
     
    def __get_cookies(self): 
        self.requests.get('https://www.pixiv.net', headers = self.__headers()) 
        cookies = self.requests.cookies.get_dict() 
        return cookies     
     
    def gen_new_headers(self): 
        update_cookies = '' 
        headers = self.__headers() 
        cookies = self.__get_cookies() 
        for k, v in cookies.items(): 
            update_cookies += f'{k}={v};' 
        headers['Cookie'] = update_cookies 
        return headers 
         
    def get_category_list(self, category): 
        response = self.requests.get( 
            f'https://www.pixiv.net/ajax/search/illustrations/{category}',  
                headers = self.headers,  
                params = { 
                    'word':category, 
                    'order':'date_d', 
                    'mode':'all', 
                    'p':1, 
                    's_mode':'s_tag_full', 
                    'type':'illust_and_ugoira', 
                    'lang':'zh_tw' 
            }).json() 
        return response 
     
    def download_img(self, image_name, image_url): 
        response = self.requests.get(image_url, headers = self.headers) 
        status = response.status_code 
        if status != 200: 
            return False 
        content = response.content 
        if not os.path.isdir('image'): 
            os.mkdir('image') 
        with codecs.open(f'image/{image_name}.jpg', 'wb')as f: 
            f.write(content) 
        return content 
         
    # def main(self, category): 
    #     response = self.get_category_list(category) 
         
    #     for data in response['body']['illust']['data']: 
    #         image_name = data['title'] 
    #         image_url = data['url'] 
    #         print(image_name, image_url) 
             
    #         self.download_img(image_name, image_url) 
    #         sleep(1)  
 
    def main(self, url): 
        response = self.requests.get(url, headers = self.headers).text 
        route = response.split('"original":"')[1].split('"')[0] 
        file_type = route.split('.')[-1] 
        image_url = route 
        i = 1 
        while True: 
            print(image_url) 
            content = self.download_img(i, image_url) 
            if not content: 
                break 
            image_url = route.replace(f'p0.{file_type}', f'p{i}.{file_type}') 
            i += 1 
             
             
if __name__ == '__main__': 
    pageID = '97198700' 
    pixiv = Pixiv().main(f'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pageID}')