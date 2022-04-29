from scraper import Danbooru
import time

start_time = time.time()
keyword = str(input("please input keyword : "))
foldername = str(input("please input folder name : "))
try:
    totalpage = int(input("please input total pages:"))
except Exception as e:
    print(e)

keyword = keyword.replace(' ','_')
d = Danbooru(keyword, totalpage, foldername)
d.scrape_bulk_images()

print('total run time :',(time.time() - start_time))