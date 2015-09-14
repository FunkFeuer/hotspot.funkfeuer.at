#!/usr/bin/env python
import os
activate_this = os.getcwd() + '/venv/bin/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))

from appsrv import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


