from flask import Flask, render_template, url_for, request, redirect
from write import Writer


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/essay', methods=['POST'])
def essay():
	keyword = request.form['keyword']

	if not keyword:
		return redirect(url_for('index'))

	essay = Writer(keyword)
	result = essay.write()

	return render_template('essay.html', result=result, essay=essay, keyword=keyword)


if __name__ == '__main__':
	app.run()