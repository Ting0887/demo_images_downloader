import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures

class Danbooru:
    def __init__(self, input_text, page, folder):
        self.input_text = input_text
        self.page = page
        self.folder = folder

    # when you want to scrape many pages, you can try it
    def scrape_bulk_images(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            executor.submit(self.scrape_images_link)
    
    def scrape_images_link(self):
        save_link = []
        for p in range(1, self.page+1):
            url = f'https://danbooru.donmai.us/posts?page={p}&tags={self.input_text}'
            res = requests.get(url)
            soup = BeautifulSoup(res.text,'lxml')
            all_images = soup.find_all('div',id='posts')[0].find_all('a','post-preview-link')
            if all_images == []:
                print('image not found, try other keyword')
                break
            for image in all_images:
                image_link = 'https://danbooru.donmai.us' + image['href'].split('?')[0] 
                save_link.append(image_link)  

        self.download_images(save_link)

    def download_images(self, save_link):
        self.build_folder()
        for link in save_link:
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'lxml')
            img = soup.select('#content')[0].find('img')['src']
            self.save_images(img)

    def build_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def save_images(self, img):
        img_content = requests.get(img).content
        img_filename = img.split('/')[-1]
        with open(f"{self.folder}/{img_filename}",'wb') as f:
            f.write(img_content)