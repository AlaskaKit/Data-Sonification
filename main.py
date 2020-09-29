from sanic import Sanic
from sanic.response import file, html, json, redirect
from jinja2 import Template
import aiofiles

import os

from sanic.views import HTTPMethodView

app = Sanic(__name__)

app.static('/static', './static')

os.path.join('./xls_files')
config = {}
config["xls_files"] = "./xls_files"


class SimpleView(HTTPMethodView):
	
	def render_template(self, html_name, **args):
		with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f:
			html_text = f.read()
		template = Template(html_text)
		return html(template.render(args))
	
	def get(self, request):
		return self.render_template('index.html')
	
	def post(self, request):
		uploaded_file = request.files.get('xlsfile')
		file_parameters = {
			'body': uploaded_file.body,
			'name': uploaded_file.name,
			'type': uploaded_file.type
		}
		file_path = f"{config['xls_files']}" + "/" + request.files["xlsfile"][0].name
		with open(file_path, 'wb') as f:
			f.write(file_parameters['body'])
		f.close()
		
		
		
		return json({"received": True, "file_names": request.files.keys()})


app.add_route(SimpleView.as_view(), "/")

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8000, debug=True)
