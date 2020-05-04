@echo off
set FLASK_APP=flaskr
set FLASK_ENV=development
if not exist instance\flaskr.sqlite (python -m flask init-db)
python -m flask run