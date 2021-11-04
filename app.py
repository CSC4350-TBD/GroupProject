import flask
import os
from flask_sqlalchemy import SQLAlchemy
from moviedb import get_id, get_movie_info
from imdb import get_imdb_id

app = flask.Flask(__name__)


# Heroku DB Fix incase of bad db url
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
	db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/')
def index():
	return flask.render_template(
    	"index.html"
    )

#The following will probably need to be split between diffent pages, depending on how we do the routing.
#This just made it easy to make sure that the APIs work.
@app.route('/placeholder')
def main():
	search_term = "Dune" #This will need to be changed into a form request later
	imdbid, imdb_api_img = get_imdb_id(search_term)
	moviedb_id = get_id(imdbid)
	movie_genre, movie_title = get_movie_info(moviedb_id)

	return flask.render_template(
    	"index.html"					#placeholder
    )

if __name__ == "__main__":
	app.run(
        #uncomment following 2 lines once ready for deployment to heroku.
		#host=os.getenv('IP', '0.0.0.0'),
		#port=int(os.getenv('PORT', 8080)),
		debug=True
	)