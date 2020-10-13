from app import app
from flask import render_template, request


@app.errorhandler(404)
def not_found(e):
	return render_template("public/404.html"), 404


@app.errorhandler(500)
def int_error(e):
	return render_template("public/500.html"), 500
