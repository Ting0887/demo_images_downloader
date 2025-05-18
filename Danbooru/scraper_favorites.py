import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import time

headers = {
    'User-Agent': 'Mozilla/5.0',
}

class Danbooru:
    def __init__(self, page, folder, userName):
        self.page = page
        self.folder = folder
        self.userName = userName
    
    def scrape_images_link(self, page):
        save_link = []
        for p in range(1, page+1):
            url = f"https://danbooru.donmai.us/post_votes?page={p}&search%5Buser_name%5D={self.userName}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                all_images = soup.find_all('a', 'post-preview-link')
                for image in all_images:
                    image_link = 'https://danbooru.donmai.us' + image['href'].split('?')[0]
                    save_link.append(image_link)
            except:
                pass
        self.download_images(save_link)
        
    def download_images(self, save_link):
        self.build_folder()
    
        def download_single_link(link):
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                img = soup.select('#content')[0].find('img')['src']
                self.save_images(img)
            except:
                video = soup.select('#content')[0].find('video')['src']
                self.save_images(video)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(download_single_link, save_link)

    def build_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def save_images(self, img):
        img_content = requests.get(img).content
        img_filename = img.split('/')[-1]
        with open(f"{self.folder}/{img_filename}",'wb') as f:
            f.write(img_content)