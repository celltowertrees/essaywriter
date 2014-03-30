from flask import Flask, render_template, url_for, request, redirect
from write import PosSorter, MarkovWriter, TextFile


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/essay', methods=['POST'])
def essay():
    if request.method == 'POST':
        keyword = request.form['keyword']
        choice = request.form['writer_type']

        if not keyword or not choice:
            return redirect(url_for('index'))

        t = TextFile("usability_testing.txt", keyword)
        text = t.read_text()

        if choice == 'PosSorter':
            c = PosSorter(text)
            markov = False
        elif choice == 'MarkovWriter':
            c = MarkovWriter(text)
            markov = True

        result = c.analyze()

    return render_template('essay.html', result=result, markov=markov, keyword=keyword)


if __name__ == '__main__':
    app.run()
