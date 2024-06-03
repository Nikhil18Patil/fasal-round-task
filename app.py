from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify
from model import User, MovieList, Movie, Base, engine
from sqlalchemy.orm import sessionmaker , joinedload
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# @app.route('/')
# def index():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         session_db = DBSession()
        
#         user_lists = session_db.query(MovieList).filter_by(user_id=user_id).all()
#         public_lists = session_db.query(MovieList).filter_by(public=True).all()
        
#         session_db.close()
        
#         return render_template('index.html', user_lists=user_lists, public_lists=public_lists)
#     else:
#         return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session_db = DBSession()
        user = session_db.query(User).filter_by(username=username, password=password).first()
        session_db.close()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username=username, password=password, email=email, created_at=datetime.utcnow())
        session_db = DBSession()
        session_db.add(new_user)
        session_db.commit()
        session_db.close()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' in session:
        movies = []
        error = None
        # import pdb ; pdb.set_trace()
        if request.method == 'POST':
            search_params = {
                'apikey': '1346c0b2',
                's': request.form.get('search'),
                'i': request.form.get('imdb_id'),
                'type': request.form.get('type'),
                'y': request.form.get('year'),
                'plot': request.form.get('plot', 'short'),
                'r': 'json'
            }
            # Remove empty parameters
            search_params = {k: v for k, v in search_params.items() if v}

            response = requests.get('http://www.omdbapi.com/', params=search_params)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    if 'Search' in data:
                        movies = data['Search']
                    else:
                        movies = [data]
                else:
                    error = data.get('Error', 'No movies found')
            else:
                error = 'Error connecting to OMDB API'
        return render_template('search.html', movies=movies, error=error)
    else:
        return redirect(url_for('login'))   

@app.route('/create_list', methods=['GET', 'POST'])
def create_list():
    if 'user_id' in session:
        if request.method == 'POST':
            user_id = session['user_id']
            list_name = request.form['list_name']
            is_public = True if request.form.get('is_public') else False

            movie_title = request.form.get('title')
            movie_year = request.form.get('year')
            imdb_id = request.form.get('imdb_id')
            movie_type = request.form.get('type')
            plot = request.form.get('plot')
            poster = request.form.get('poster')

            session_db = DBSession()

            # Create new movie list
            new_list = MovieList(
                user_id=user_id,
                name=list_name,
                public=is_public,
                created_at=datetime.utcnow()
            )
            session_db.add(new_list)
            session_db.commit()

            # Create new movie and associate it with the list
            new_movie = Movie(
                title=movie_title,
                imdb_id=imdb_id,
                type=movie_type,
                year=movie_year,
                plot=plot,
                poster=poster,
                list_id=new_list.id
            )
            session_db.add(new_movie)
            session_db.commit()

            session_db.close()
            return redirect(url_for('index'))
        else:
            movie_details = {
                'title': request.args.get('title'),
                'year': request.args.get('year'),
                'imdb_id': request.args.get('imdb_id'),
                'type': request.args.get('type'),
                'plot': request.args.get('plot'),
                'poster': request.args.get('poster')
            }
            return render_template('create_list.html', movie_details=movie_details)
    else:
        return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        session_db = DBSession()
        user_lists = session_db.query(MovieList).filter_by(user_id=session['user_id']).filter_by(public=False).all()
        public_lists = session_db.query(MovieList).filter_by(public=True).all()
        session_db.close()
        return render_template('index.html', user_lists=user_lists, public_lists=public_lists)
    else:
        return redirect(url_for('login'))

@app.route('/list/<int:list_id>')
def get_list(list_id):
    session_db = DBSession()
    movie_list = session_db.query(MovieList).options(joinedload(MovieList.movies)).filter_by(id=list_id).first()
    if movie_list:
        if movie_list.public or movie_list.user_id == session.get('user_id'):
            response = {
                'id': movie_list.id,
                'name': movie_list.name,
                'movies': [{
                    'title': movie.title,
                    'imdb_id': movie.imdb_id,
                    'type': movie.type,
                    'year': movie.year,
                    'plot': movie.plot,
                    'poster': movie.poster
                } for movie in movie_list.movies]
            }
            session_db.close()
            return jsonify(response)
        else:
            session_db.close()
            return jsonify({'error': 'Access denied'}), 403
    else:
        session_db.close()
        return jsonify({'error': 'List not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
