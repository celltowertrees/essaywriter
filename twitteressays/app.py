from flask import Flask, render_template, url_for, request, redirect
from write import MarkovWriter, Tweets


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

    t = Tweets(keyword)
    text = t.extract_tweets()
    m = MarkovWriter(text)
    result = m.generateModel()

    markov = True

    return render_template('essay.html', result=result, markov=markov, keyword=keyword)


if __name__ == '__main__':
    app.run()
