
repo-init: pip-install translations_compile

venv:
	test -d venv || virtualenv venv

pip-install: venv
	. venv/bin/activate; venv/bin/pip install -U Flask Flask-Cache Flask-Babel git+https://github.com/oe1rfc/unifi-api.git

run_debug:
	./run_debug.py

uwsgi:
	uwsgi --ini uwsgi.ini

translations_update: venv
	. venv/bin/activate; pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	. venv/bin/activate; pybabel update -i messages.pot -d appsrv/translations
	rm messages.pot
	
translations_compile: venv
	. venv/bin/activate; pybabel compile -d appsrv/translations

