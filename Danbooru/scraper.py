import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures

class DanbooruScraper:
    base_url = "https://danbooru.donmai.us"
    max_workers = 6  # Max threads for downloading

    def __init__(self, page, folder):
        self.page = page
        self.folder = folder

    def build_folder(self):
        os.makedirs(self.folder, exist_ok=True)

    def save_image(self, img_url):
        """Save an image to the target folder."""
        try:
            img_content = requests.get(img_url, timeout=10).content
            img_filename = os.path.join(self.folder, img_url.split('/')[-1])
            with open(img_filename, 'wb') as f:
                f.write(img_content)
            print(f"Saved: {img_filename}")
        except Exception as e:
            print(f"Failed to save image {img_url}: {e}")

    def download_images(self, image_links):
        """Download images using multithreading."""
        self.build_folder()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.process_image_link, image_links)

    def process_image_link(self, link):
        """Process a single image link and download the image."""
        try:
            res = requests.get(link, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')
            img_url = soup.select_one('#content img')['src']
            self.save_image(img_url)
        except Exception as e:
            print(f"Failed to process link {link}: {e}")


class DanbooruUserFav(DanbooruScraper):
    def __init__(self, page, folder, username):
        super().__init__(page, folder)
        self.username = username

    def scrape_images(self):
        image_links = []
        for p in range(1, self.page + 1):
            url = f"{self.base_url}/post_votes?page={p}&search%5Buser_name%5D={self.username}"
            print(f"Fetching: {url}")
            try:
                res = requests.get(url, timeout=10)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'lxml')
                all_images = soup.find_all('a', 'post-preview-link')
                image_links.extend([self.base_url + img['href'] for img in all_images])
            except Exception as e:
                print(f"Failed to fetch page {p}: {e}")
        self.download_images(image_links)

class DanbooruArtistWork(DanbooruScraper):
    def __init__(self, page, folder, artistname):
        super().__init__(page, folder)
        self.artistname = artistname

    def scrape_images(self):
        image_links = []
        for p in range(1, self.page + 1):
            url = f"{self.base_url}/posts?page={p}&tags={self.artistname}"
            print(f"Fetching: {url}")
            try:
                res = requests.get(url, timeout=10)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'lxml')
                all_images = soup.find('div', id='posts').find_all('a', 'post-preview-link')
                image_links.extend([self.base_url + img['href'] for img in all_images])
            except Exception as e:
                print(f"Failed to fetch page {p}: {e}")
        self.download_images(image_links)
