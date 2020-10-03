from app import app
from flask.views import MethodView
from flask import render_template, request, redirect
import os

app.config["XLS_UPLOADS"] = './app/xls_files'

class BasicView(MethodView):
	
	def get(self):
		return render_template("public/index.html")
	
	def post(self):
		if request.form:
			duration = request.form['set_duration']
		else:
			raise NotImplementedError
		
		if request.files:
			xlsfile = request.files["xlsfile"]
			xlsfile.save(os.path.join(app.config["XLS_UPLOADS"], xlsfile.filename))
			return redirect(request.url)
		else:
			raise NotImplementedError
		
		
		# uploaded_file = request.files.get('xlsfile')
		# file_parameters = {
		# 	'body': uploaded_file.body,
		# 	'name': uploaded_file.name,
		# 	'type': uploaded_file.type
		# }
		#
		# file_path = os.path.join("./xls_files", f"{request.files['xlsfile'][0].name}")
		# with open(file_path, 'wb') as f:
		# 	f.write(file_parameters['body'])
		# f.close()
		# filename = file_path.split("\\")[-1]
		#
		# process = SonificationCycle(filename, float(duration))
		# wav_path = os.path.join("./wav_files", f"{filename}.wav")
		#
		# return file_stream(wav_path)

	
app.add_url_rule('/', view_func=BasicView.as_view('BasicView'))
