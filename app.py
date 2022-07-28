from distutils.log import debug
from flask import Flask ,render_template, request, redirect, url_for
import numpy as np
import pickle

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            votes = list(popular_df['number_of_ratings'].values),
                            rating = list(popular_df['average_ratings'].values))

@app.route('/Recommend',methods=["GET","POST"])
def recommend():
    if request.method == 'POST':
        user_input = request.values['user_input']
        data = []
        if(len(np.where(pt.index == user_input)[0])):
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
            
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)
            f = 1
        else:
            f = 0
        return render_template('recommend.html',data=data,f =f)
    else:
        return render_template('recommend.html')


@app.route('/Searchbooks')
def searchbooks():
    return render_template('spselection.html')

@app.route("/Topfiftybooks")
def topfiftybooks():
    return render_template('topbooks.html',book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            votes = list(popular_df['number_of_ratings'].values),
                            rating = list(popular_df['average_ratings'].values))

if __name__ == "__main__":
    app.run(debug = True)