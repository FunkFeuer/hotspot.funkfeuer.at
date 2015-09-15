import time, re
from os.path import isfile

from flask import render_template, request, redirect, abort

from appsrv import (app, cache)

from unifi.controller import Controller

c = Controller(app.config.get('UNIFI_CTRL_URL', 'localhost'),
               app.config.get('UNIFI_CTRL_USER', 'root'),
               app.config.get('UNIFI_CTRL_PASSWORD', ''),
               app.config.get('UNIFI_CTRL_PORT', 8443),
               "v4")

@app.route('/guest/s/<site>/', methods=['GET', 'POST'])
def guest_splash(site):
    
    if not check_args(request.args):
        app.logger.debug('check_args() failed.')
        abort(418)
    
    # if timestamp is more than 10 minutes off, we redirect the client to the 
    # URL he was requesting
    if (abs(int(time.time()) - int(request.args.get('t'))) > 10*60 and not app.debug):
        app.logger.debug('%s: timestamp too old (%s, %s)' % (request.args.get('id'), int(time.time()), request.args.get('t')) )
        return redirect(request.args.get('url'), code=307)
    
    if site not in get_sites():
        app.logger.debug('%s: unknown site: %s' % (request.args.get('id'), site) )
        abort(404)
    
    if request.args.get('abort') == 'true':
        # disconnect user from AP TODO: deauth attack
        app.logger.debug('%s: disconnecting user' % request.args.get('id'))
        c.disconnect_client(request.args.get('id'), site_id=site)
    
    templatepath = 'default'
    if request.method == 'POST':
        # TOS accepted

        # make sure to consume POST data
        data = request.data

        if isfile('%s/templates/%s/accepted.html' % (app.root_path, site)):
            templatepath = site
        
        if not app.debug:
            c.authorize_guest(
                guest_mac       = request.args.get('id'),
                minutes         = app.config.get('TIME_LIMIT'),
                up_bandwidth    = app.config.get('UPLOAD_BANDWIDTH'),
                down_bandwidth  = app.config.get('DOWNLOAD_BANDWIDTH'),
                byte_quota      = app.config.get('TRAFFIC_LIMIT'),
                ap_mac          = request.args.get('ap'),
                site_id         = site
                );
        return render_template(templatepath + '/accepted.html')
    
    else:
        # splash page
        if isfile('%s/templates/%s/splash.html' % (app.root_path, site)):
            templatepath = site
        return render_template(templatepath + '/splash.html')



@cache.cached(timeout=600, key_prefix='unifi_ctrl_get_sites')
def get_sites():
    return (site['name'] for site in c.get_sites())

def check_mac(mac):
    return bool(re.match("^([0-9a-f]{2}:){5}([0-9a-f]{2})$", mac))

def check_args(args):
    return check_mac(args.get('ap')) & check_mac(args.get('id'))


