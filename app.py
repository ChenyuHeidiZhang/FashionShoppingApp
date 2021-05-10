from flask import Flask , render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from model import Retriever
import pandas as pd
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ywvjauzaqnbaba:20e72e3ea0983dfe5b7b826d64c15106615e0746b1ee221a05ec84fba94607ba@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d6ss3m0ohsoq9t'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = "items"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    color = db.Column(db.Text, nullable=False)
    text_repr = db.Column(db.ARRAY(db.Float), nullable=False)
    img_repr = db.Column(db.ARRAY(db.Float), nullable=False)

    def __init__(self, description, img_url, url, brand, price, color, text_repr, img_repr):
        self.description = description
        self.img_url = img_url
        self.url = url
        self.brand = brand
        self.price = price
        self.color = color
        self.text_repr = text_repr
        self.img_repr = img_repr

    def __repr__(self):
        return f"{self.description}: {self.url}"

    def to_dict(self):
        return {
            'description': self.description,
            'img_url': self.img_url,
            'url': self.url,
            'brand': self.brand,
            'price': self.price,
            'color': self.color,
            'text_repr': self.text_repr,
            'img_repr': self.img_repr
        }


# Control will come here and then gets redirect to the index function
@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index", methods = ["GET", "POST"])
def index():
    if request.method == 'POST': # When a user clicks submit button it will come here.
        items_data = Item.query.all()
        df = pd.DataFrame.from_records([item.to_dict() for item in items_data])
        print(df.head())
        print("Construsting retriever...")
        retriever = Retriever(df)
        print("Done")

        data = request.form # gets the data from the form in index.html file
        text = data["input_text"]
        img_url = data["input_img_url"]
        if text != '':
            top_items = retriever.retrieve(text, mode='text')
        else:
            top_items = retriever.retrieve(img_url, mode='img')

        return render_template("index.html", retrieved_items = top_items) # passes top_items variable into the index.html file.

    return render_template("index.html")


if __name__=="__main__":
    #db.create_all()
    app.run(debug=True)

