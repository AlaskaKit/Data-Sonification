from sanic import Sanic
from sanic.response import file, html, file_stream
from jinja2 import Template
from sonification_cycle import SonificationCycle

import os

from sanic.views import HTTPMethodView

app = Sanic(__name__)

app.static('/static', './static')

# os.path.join('./xls_files')
# config = {}
# config["xls_files"] = "./xls_files"

#app.config['KEEP_ALIVE_TIMEOUT'] = 60



class SimpleView(HTTPMethodView):
	
	def render_template(self, html_name, **args):
		with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f:
			html_text = f.read()
		template = Template(html_text)
		return html(template.render(args))
	
	def get(self, request):
		return self.render_template('index.html')
	
	def post(self, request):
		
		duration = request.form['set_duration'][0]
		print(duration)
		uploaded_file = request.files.get('xlsfile')
		file_parameters = {
			'body': uploaded_file.body,
			'name': uploaded_file.name,
			'type': uploaded_file.type
		}
		# file_path = f"{config['xls_files']}" + "/" + request.files["xlsfile"][0].name
		file_path = os.path.join("app/xls_files", f"{request.files['xlsfile'][0].name}")
		with open(file_path, 'wb') as f:
			f.write(file_parameters['body'])
		f.close()
		filename = file_path.split("\\")[-1]
		
		process = SonificationCycle(filename, float(duration))
		wav_path = os.path.join("app/wav_files", f"{filename}.wav")
		
		return file_stream(wav_path)


app.add_route(SimpleView.as_view(), "/")

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8000, debug=True)
