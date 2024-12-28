from django.shortcuts import render
from flask import Flask, render_template, request
from scraper import DanbooruArtistWork
from scraper import DanbooruUserFav
import time

app = Flask('__name__', 
            template_folder='template',
            static_folder = 'static',
            static_url_path='/static')

@app.route('/search_artistwork',methods=["GET","POST"])
def download_artistWork():
    if request.method == 'POST':
        keyword = str(request.form.get('keyword')).replace(' ','_')
        try:
            num_page = int(request.form.get('num_page'))
        except Exception as e:
            num_page = request.form.get('num_page')
            print(e)
        folder_name = str(request.form.get('folderpath'))
        start = time.time()
        DanbooruArtistWork(num_page, folder_name, keyword).scrape_images()
        end = time.time()
        spend_time = round(end-start, 2)    
        return render_template("search_artist.html",keyword=keyword, 
                                num_page=num_page,
                                folder_name=folder_name, 
                                spend_time=spend_time)
    else:
        return render_template("search_artist.html")

@app.route('/search_userfav',methods=["GET","POST"])
def download_userFav():
    if request.method == 'POST':
        keyword = str(request.form.get('keyword')).replace(' ','_')
        try:
            num_page = int(request.form.get('num_page'))
        except Exception as e:
            num_page = request.form.get('num_page')
            print(e)
        folder_name = str(request.form.get('folderpath'))
        start = time.time()
        DanbooruUserFav(num_page, folder_name, keyword).scrape_images()
        end = time.time()
        spend_time = round(end-start, 2)    
        return render_template("search_user.html",keyword=keyword, 
                                num_page=num_page,
                                folder_name=folder_name, 
                                spend_time=spend_time)
    else:
        return render_template("search_user.html")


@app.route('/home',methods=['GET','POST'])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, port='8844')
