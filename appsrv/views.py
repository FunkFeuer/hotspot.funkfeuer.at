import os
from flask import render_template, send_from_directory
from appsrv import (app, cache)

from controllers import unifi_ctrl


@app.route('/')
@cache.cached(timeout=7200)
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
@cache.cached(timeout=7200)
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# custom error handlers
#@app.errorhandler(405)
#def err_405(e):
#    return render_template('error-405.html'), 405

#@app.errorhandler(404)
#def err_404(e):
#    return render_template('error-404.html'), 404

#@app.errorhandler(403)
#def err_403(e):
#    return render_template('error-403.html'), 403
