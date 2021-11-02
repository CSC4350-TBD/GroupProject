import flask
import os
from flask_sqlalchemy import SQLAlchemy

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


if __name__ == "__main__":
	app.run(
        #uncomment following 2 lines once ready for deployment to heroku.
		#host=os.getenv('IP', '0.0.0.0'),
		#port=int(os.getenv('PORT', 8080)),
		debug=True
	)