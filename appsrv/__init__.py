from flask import Flask, request
from flask.ext.cache import Cache
from flask.ext.babel import Babel

try:
	import appsrv.settings
except:
	import appsrv.settings_sample as settings

# flask app
app = Flask(__name__)
babel = Babel(app)

app.config.from_object(settings)

# create cache instance
cache = Cache()

@app.before_first_request
def cacheinit():
	if app.debug:
		# no caching if in debug mode
		app.config['CACHE_TYPE'] = 'null'
	cache.init_app(app)

# import views
import appsrv.views

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match([str(translation) for translation in babel.list_translations()])

