from sanic import Sanic
from sanic.response import file, html
from jinja2 import Template

import os


app = Sanic(__name__)

app.static('/static', './static')


def render_template(html_name, **args):
	with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f:
		html_text = f.read()
	template = Template(html_text)
	return html(template.render(args))


@app.route("/")
async def index(request):
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8000)