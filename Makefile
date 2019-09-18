DEV_PASSWORD=sevilla
DEV_SECRET_KEY=dev-secret-key
DEV_DB_URI=sqlite:///$(shell realpath sevilla.db)

dev_server:
	FLASK_APP=sevilla \
	FLASK_ENV=development \
	SECRET_KEY=$(DEV_SECRET_KEY) \
	SESSION_COOKIE_SECURE=False \
	SEVILLA_PASSWORD=$(DEV_PASSWORD) \
	SQLALCHEMY_DATABASE_URI=$(DEV_DB_URI) \
	flask run --host 0.0.0.0 --port 8080

gunicorn_server:
	SECRET_KEY=$(DEV_SECRET_KEY) \
	SESSION_COOKIE_SECURE=False \
	SEVILLA_PASSWORD=$(DEV_PASSWORD) \
	SQLALCHEMY_DATABASE_URI=$(DEV_DB_URI) \
	gunicorn "sevilla:create_app()" -b 0.0.0.0:8080

shell:
	FLASK_APP=sevilla \
	SEVILLA_PASSWORD=$(DEV_PASSWORD) \
	SQLALCHEMY_DATABASE_URI=$(DEV_DB_URI) \
	flask shell

routes:
	FLASK_APP=sevilla \
	flask routes

test:
	python3 -m unittest

lint:
	flake8 sevilla/ tests/ migrations/
	black --check sevilla/ tests/

format:
	black sevilla/ tests/

deploy:
	git push heroku master

setup-jshint:
	npm install jshint@2.10.2

jshint:
	node_modules/jshint/bin/jshint sevilla/static/*.js
