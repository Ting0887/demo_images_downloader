from threading import local
from flask import Flask, render_template, request
from scraper import Danbooru
from scraper import url_encode
import time

app = Flask('__name__', 
            template_folder='template',
            static_folder = 'static',
            static_url_path='/static')

@app.route('/danbooru_images_demo',methods=["GET","POST"])
def download():
    if request.method == 'POST':
        keyword = str(request.form.get('keyword'))
        
        # if keyword only have _
        if " " in keyword:
            split_kws = keyword.split(" ")
            final_keyword = split_kws[0] + "+" + split_kws[1]
        else:
            final_keyword = keyword
        try:
            num_page = int(request.form.get('num_page'))
        except Exception as e:
            num_page = request.form.get('num_page')
        
        folder_name = str(request.form.get('folderpath'))
        start = time.time()
        
        danb = Danbooru(final_keyword, num_page, folder_name)
        
        # check image can be found
        Notfound_err = danb.check_notfound()
        if "image not found, try other keyword" in Notfound_err:
            return render_template("Home.html", Notfound_err=Notfound_err)
        else:
            danb.scrape_bulk_images() 
            end = time.time()
            spend_time = round(end-start, 2)
            return render_template("Home.html",**locals())
    else:
        return render_template("Home.html")

if __name__ == '__main__':
    app.run(port='8844', debug=True)