from app import app
from flask.views import MethodView
from flask import render_template, request, redirect, send_from_directory, abort, flash
from werkzeug.utils import secure_filename
import os

from sonification_cycle import SonificationCycle


class BasicView(MethodView):
	"""
	Main view of the web app ("/" route).
	On the GET request renders the index page.
	On the POST request:
		- checks if there is a correct duration value
		- checks if there is a file in a proper format with a safe filename
		- saves user's source file to the directory set up in the config
		- gives the path to the source file to the SonificationCycle instance
		- in case of success reads the path to the *.wav output file and redirects user to the get_wav route
		- in case of any errors flashes the content of the error and redirects to index again.
	"""
	def allowed_ext(self, filename):
		
		if not "." in filename:
			return False
		
		ext = filename.rsplit(".", 1)[1]
		
		if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
			return True
		else:
			return False
	
	def get(self):
		return render_template("public/index.html")
	
	def post(self):
		if request.form:
			received_duration = request.form['set_duration']
			try:
				duration = float(received_duration)
			except ValueError:
				flash("Duration in seconds must be a number from 10 to 999.", "danger")
				return redirect(request.url)
			if 999 < duration or duration < 10:
				flash("Duration in seconds must be a number from 10 to 999.", "danger")
				return redirect(request.url)
			
		else:
			flash("Duration in seconds must be a number from 10 to 999.", "danger")
			return redirect(request.url)
		
		if request.files:
			srcfile = request.files["srcfile"]
			
			if srcfile.filename == "":
				flash("Attach a file in a proper format (*.xls, *.xlsx, *.csv).", "danger")
				return redirect(request.url)
				
			if self.allowed_ext(srcfile.filename):
				name = secure_filename(srcfile.filename)
				srcpath = os.path.join(app.config["SRC_UPLOADS"], name)
				srcfile.save(srcpath)
				
				try:
					process = SonificationCycle(srcpath, duration)
					process.perform_cycle()
				except Exception as e:
					flash(f"{str(e)}", "danger")
					return redirect(request.url)
				
				wav_path = process.path_to_wav
				wavname = os.path.split(wav_path)[1]
				return redirect(f"get_wav/{wavname}")
			else:
				flash("Attach a file in a proper format (*.xls, *.xlsx, *.csv).", "danger")
				return redirect(request.url)
		else:
			flash("Attach a file in a proper format (*.xls, *.xlsx, *.csv).", "danger")
			return redirect(request.url)
	
		
class ResultView(MethodView):
	"""
	A get_wav view. Takes the path, offers the user to save the file (if there is any) or throws a 404
	(if there is no such file on this path).
	"""
	def get(self, path):
		
		try:
			return send_from_directory(
				app.config["WAV_FILES"], filename=path, as_attachment=True
			)
			
		except FileNotFoundError:
			abort(404)


app.add_url_rule('/', view_func=BasicView.as_view('BasicView'), methods=['GET', 'POST', ])
app.add_url_rule('/get_wav/<path:path>', view_func=ResultView.as_view('ResultView'), methods=['GET', ])
