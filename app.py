from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
import requests
from bson.objectid import ObjectId # นำเข้า ObjectId เพื่อจัดการ ID ของ MongoDB

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient('mongodb', 27017)
db = client['movie_database']
movies_collection = db['movies']

# TMDb API Configuration
TMDB_API_KEY = 'eba1b3fab26d44fd505d2677d44ee447'
TMDB_API_URL = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query='
TMDB_BASE_POSTER_URL = 'https://image.tmdb.org/t/p/w500'

# Route สำหรับหน้าหลัก: แสดงรายการภาพยนตร์ทั้งหมดและโปรไฟล์ทีมงาน
@app.route('/')
def index():
    movies = list(movies_collection.find())
    return render_template('index.html', movies=movies)

# Route สำหรับเพิ่มข้อมูลภาพยนตร์
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        release_year = request.form['release_year'] 

        search_url = f'{TMDB_API_URL}{title}&year={release_year}'
        
        try:
            response = requests.get(search_url)
            search_results = response.json()
            
            if search_results and 'results' in search_results and search_results['results']:
                first_result = search_results['results'][0]
                
                imdb_score = first_result.get('vote_average', 0.0)
                rotten_tomato_score = 0.0 
                
                poster_path = first_result.get('poster_path')
                poster_url = f"{TMDB_BASE_POSTER_URL}{poster_path}" if poster_path else 'https://placehold.co/500x750/cccccc/333333?text=No+Poster'

                new_movie = {
                    'title': first_result.get('title', title),
                    'release_year': int(first_result.get('release_date', '0000')[:4]),
                    'imdb_score': imdb_score,
                    'rotten_tomato_score': rotten_tomato_score,
                    'poster_url': poster_url
                }

                movies_collection.insert_one(new_movie)
                
            else:
                print(f"Movie '{title}' (Year: {release_year}) not found on TMDb.")
                new_movie = {
                    'title': title,
                    'release_year': int(release_year),
                    'imdb_score': 0.0,
                    'rotten_tomato_score': 0.0,
                    'poster_url': 'https://placehold.co/500x750/cccccc/333333?text=No+Poster'
                }
                movies_collection.insert_one(new_movie)
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from TMDb API: {e}")
            new_movie = {
                'title': title,
                'release_year': int(release_year),
                'imdb_score': 0.0,
                'rotten_tomato_score': 0.0,
                'poster_url': 'https://placehold.co/500x750/cccccc/333333?text=API+Error'
            }
            movies_collection.insert_one(new_movie)
            
        return redirect(url_for('index'))

# Route สำหรับลบข้อมูลภาพยนตร์
@app.route('/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(movie_id):
    try:
        # แปลง string ID จาก URL ให้เป็น ObjectId ก่อนนำไปค้นหาใน MongoDB
        movies_collection.delete_one({'_id': ObjectId(movie_id)})
    except Exception as e:
        print(f"Error deleting movie: {e}")
    return redirect(url_for('index'))

# Route สำหรับแก้ไขข้อมูลภาพยนตร์ (GET: แสดงฟอร์ม, POST: อัปเดตข้อมูล)
@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    try:
        movie_obj_id = ObjectId(movie_id)
    except Exception:
        return redirect(url_for('index')) # หาก ID ไม่ถูกต้องให้กลับไปหน้าหลัก

    if request.method == 'POST':
        # รับข้อมูลที่ถูกแก้ไขจากฟอร์ม
        title = request.form['title']
        release_year = request.form['release_year']
        imdb_score = float(request.form['imdb_score'])
        rotten_tomato_score = float(request.form['rotten_tomato_score'])
        poster_url = request.form['poster_url']

        # อัปเดตข้อมูลใน MongoDB
        movies_collection.update_one(
            {'_id': movie_obj_id},
            {'$set': {
                'title': title,
                'release_year': int(release_year),
                'imdb_score': imdb_score,
                'rotten_tomato_score': rotten_tomato_score,
                'poster_url': poster_url
            }}
        )
        return redirect(url_for('index'))
    else:
        # GET request: ดึงข้อมูลภาพยนตร์มาแสดงในฟอร์มแก้ไข
        movie = movies_collection.find_one({'_id': movie_obj_id})
        if movie:
            return render_template('edit_movie.html', movie=movie)
        return redirect(url_for('index')) # หากหาภาพยนตร์ไม่เจอให้กลับไปหน้าหลัก

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
