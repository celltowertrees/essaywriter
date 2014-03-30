from flask import Flask, render_template, url_for, request, redirect
from write import PosSorter, TextFile


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

    t = TextFile("usability_testing.txt", keyword)
    text = t.read_text()
    p = PosSorter(text)
    result = p.analyze()

    markov = False

    return render_template('essay.html', result=result, markov=markov, keyword=keyword)


if __name__ == '__main__':
    app.run()
