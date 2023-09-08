import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures

headers = {'User-Agent': 'Mozilla/5.0'}

class Danbooru:
    def __init__(self, input_text, page, folder):
        self.input_text = input_text
        self.page = page
        self.folder = folder
   
    def check_notfound(self):
        url = f'https://danbooru.donmai.us/posts?&tags={self.input_text}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text,'lxml')
        all_images = soup.find_all('div',id='posts')[0].find_all('a','post-preview-link')
        if all_images == []:
            return 'image not found, try other keyword'
        else:
            return 'image can be found'
    # when you want to scrape many pages, you can try it
    def scrape_bulk_images(self):
        save_link = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            # 提交多个任务，每个任务爬取一页的图片链接
            futures = [executor.submit(self.scrape_images_link, page) for page in range(1, self.page + 1)]
            # 收集所有任务的结果
            for future in concurrent.futures.as_completed(futures):
                save_link.extend(future.result())

        self.download_images(save_link)
    
    def scrape_images_link(self, page):
        url = f'https://danbooru.donmai.us/posts?page={page}&tags={self.input_text}'
        print(url)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        all_images = soup.find_all('div', id='posts')[0].find_all('a', 'post-preview-link')
        save_link = []
        for image in all_images:
            image_link = 'https://danbooru.donmai.us' + image['href'].split('?')[0]
            save_link.append(image_link)
        return save_link

    def download_images(self, save_link):
        self.build_folder()
    
        def download_single_link(link):
            res = requests.get(link, headers=headers)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                img = soup.select('#content')[0].find('img')['src']
                self.save_images(img)
            except:
                video = soup.select('#content')[0].find('video')['src']
                self.save_images(video)

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(download_single_link, save_link)


    def build_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def save_images(self, img):
        img_content = requests.get(img, headers=headers).content
        img_filename = img.split('/')[-1]
        with open(f"{self.folder}/{img_filename}",'wb') as f:
            f.write(img_content)