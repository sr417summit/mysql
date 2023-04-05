import string
from flask import Flask, render_template, request, redirect, url_for, session
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

app = Flask(__name__, static_folder='static', static_url_path='')

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
app.secret_key = 'secret'

stop_words = set(stopwords.words('english'))

docs = []
doc_count = 0



@app.route('/')
def index():
    global doc_count
    session['doc_count'] = doc_count
    return render_template('index.html', doc_count=session.get('doc_count', 0))

@app.route('/search', methods=['GET', 'POST'])
def search():
    global doc_count
    if request.method == 'POST':
        text = request.form['text']
        docs.append(text)
        doc_count += 1
        session['docs'] = docs
        session['doc_count'] = doc_count
        
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))

        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in stop_words]

        ps = PorterStemmer()
        stemmed_words = [ps.stem(word) for word in filtered_words]

        query = request.form.get('query')
        if query:
            query = query.lower()
            query = query.translate(str.maketrans('', '', string.punctuation))
            query_words = word_tokenize(query)
            filtered_query_words = [word for word in query_words if word not in stop_words]
            stemmed_query_words = [ps.stem(word) for word in filtered_query_words]

            results = []
            for doc_num, doc in enumerate(docs):
                doc_text = doc.lower()
                doc_text = doc_text.translate(str.maketrans('', '', string.punctuation))
                doc_words = word_tokenize(doc_text)
                filtered_doc_words = [word for word in doc_words if word not in stop_words]
                stemmed_doc_words = [ps.stem(word) for word in filtered_doc_words]
                for i, word in enumerate(stemmed_doc_words):
                    if word in stemmed_query_words:
                        context = ' '.join(stemmed_doc_words[max(0, i-5):i+6])
                        result = {'doc_number': doc_num+1, 'context': context, 'line_number': i+1}
                        results.append(result)

            if len(results) > 0:
                return render_template('search.html', results=results, query=query, doc_count=doc_count)
            else:
                error_message = "No matches found for your query."
                return render_template('search.html', error=error_message, doc_count=doc_count)
        else:
            if doc_count > 0:
                return render_template('search.html', doc_count=doc_count)
            else:
                error_message = "There are no documents to search."
                return render_template('search.html', error=error_message, doc_count=doc_count)
    else:
        return render_template('index.html', doc_count=session.get('doc_count', 0))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/count', methods=['POST'])
def count():
    text = request.form['text']
    char_count = len(text)
    space_count = text.count(' ')
    special_char_count = text.count('+') + text.count('-') + text.count('$') + text.count('*')
    return render_template('count.html', char_count=char_count, space_count=space_count, special_char_count=special_char_count)

@app.route('/input_text')
def input_text():
    return render_template('input.html')

@app.route('/output', methods=['POST'])
def output():
    text = request.form['text']

    # Count number of unique words
    words = text.split()
    unique_words = set(words)
    num_words = len(words)
    num_unique_words = len(unique_words)

    # Count number of spaces
    num_spaces = text.count(' ')

    # Count number of special characters
    special_chars = ['+', '-', '$', '*']
    num_special_chars = sum(text.count(char) for char in special_chars)

    return render_template('output.html',
                           text=text,
                           num_words=num_words,
                           num_unique_words=num_unique_words,
                           num_spaces=num_spaces,
                           num_special_chars=num_special_chars)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)