from app import app
from flask.views import MethodView, View
from flask import render_template, request, redirect, send_from_directory, abort
from werkzeug.utils import secure_filename
import os

from sonification_cycle import SonificationCycle


class BasicView(MethodView):
	
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
			# TODO: проверка типа
			duration = float(received_duration)
		else:
			raise NotImplementedError
		
		if request.files:
			xlsfile = request.files["xlsfile"]
			
			if xlsfile.filename == "":
				raise NotImplementedError
				
			if self.allowed_ext(xlsfile.filename):
				name = secure_filename(xlsfile.filename)
				xlspath = os.path.join(app.config["XLS_UPLOADS"], name)
				xlsfile.save(xlspath)
				# filename = xlspath.split("\\")[-1]
				process = SonificationCycle(xlspath, duration)
				wav_path = os.path.join(app.config["WAV_FILES"], f"{name}.wav")
				return redirect(f"get_wav/{wav_path}")
			else:
				raise NotImplementedError
		else:
			raise NotImplementedError


app.add_url_rule('/', view_func=BasicView.as_view('BasicView'))


@app.route("/get_wav/<path:path>")
def get_wav(path):
	
	try:
		return send_from_directory(
			app.config["WAV_FILES"], filename=path, as_attachment=True
		)
	except FileNotFoundError:
		abort(404)
	
		


