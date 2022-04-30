from threading import local
from flask import Flask, render_template, request
from scraper import Danbooru
import time

app = Flask('__name__', 
            template_folder='template',
            static_folder = 'static',
            static_url_path='/static')

@app.route('/danbooru_images_demo',methods=["GET","POST"])
def download():
    if request.method == 'POST':
        keyword = str(request.form.get('keyword')).replace(' ','_')
        try:
            num_page = int(request.form.get('num_page'))
        except Exception as e:
            num_page = request.form.get('num_page')
            print(e)
        folder_name = str(request.form.get('folderpath'))
        start = time.time()
        Danbooru(keyword, num_page, folder_name).scrape_bulk_images() 
        end = time.time()
        spend_time = round(end-start, 2)
        return render_template("Home.html",**locals())
    else:
        return render_template("Home.html")

if __name__ == '__main__':
    app.run(port='8844')