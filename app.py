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
def home():
    return render_template('home.html')

@app.route('/count', methods=['POST'])
def count():
    text = request.form['text']
    total_chars = len(text)
    upper_chars = sum(1 for char in text if char.isupper())
    spaces = sum(1 for char in text if char.isspace())
    punctuation = sum(1 for char in text if char in '.,:?$()-&')
    numbers = sum(1 for char in text if char.isdigit())

    return render_template('result.html', total_chars=total_chars, upper_chars=upper_chars, spaces=spaces, punctuation=punctuation, numbers=numbers)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/output', methods=['POST'])
def output():
    text = request.form['text']
    
    # remove punctuation and numbers
    text = ''.join(c for c in text if c.isalpha() or c.isspace())
    
    # change all letters to upper case
    text = text.upper()
    
    # count number of characters
    n = len(text)
    
    return render_template('output.html', result=text, count=n)

@app.route('/input1')
def input1():
    return render_template('input1.html')

@app.route('/count1', methods=['POST'])
def count1():
    input_s = request.form['input_s']
    input_t = request.form['input_t']

    # Clean up input text T by removing punctuation
    input_t = ''.join(char for char in input_t if char.isalnum() or char.isspace())
    input_t = input_t.upper()

    # Count occurrences of words from input S in input T
    word_counts = {}
    for word in input_s.split():
        word_counts[word] = input_t.count(word.upper())

    # Get the total count of all occurrences
    total_count = sum(word_counts.values())

    return render_template('output1.html', input_s=input_s, input_t=input_t, word_counts=word_counts, total_count=total_count)

@app.route('/input2')
def input2():
    return render_template('input2.html')

@app.route('/count2', methods=['POST'])
def count2():
    words = request.form['words']
    text = request.form['text']
    
    # Remove punctuation and convert to uppercase
    for char in text:
        if not char.isalpha() and char != ' ':
            text = text.replace(char, '')
    text = text.upper()
    
    # Count occurrences and offsets of word pairs
    word1, word2 = words.split()
    count = 0
    offsets = []
    for i in range(len(text)-1):
        if text[i:i+len(word1)] == word1 and text[i+len(word1):i+len(word1)+len(word2)] == word2:
            count += 1
            offsets.append(i)
        elif text[i:i+len(word2)] == word2 and text[i+len(word2):i+len(word2)+len(word1)] == word1:
            count += 1
            offsets.append(i)
    
    # Display results
    return render_template('output2.html', count=count, offsets=offsets, text=text)

if __name__ == '__main__':
    app.run(debug=True)



"""""
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
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)