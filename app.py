from flask import Flask, request, render_template, redirect,Markup
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
# オブジェクト変更追跡システム無効設定
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyでデータベースに接続する
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Comment(db.Model):
    """[テーブルの定義を行うクラス]
    Arguments:
        db {[Class]} -- [ライブラリで用意されているクラス]
    """

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text())
    comment = db.Column(db.Text())

    def __init__(self, pub_date, name, comment):
        """[テーブルの各カラムを定義する]
        [Argument]
            id_ -- 投稿番号(プライマリキーなので、自動で挿入される)
            pub_date -- 投稿日時
            name -- 投稿者名
            comment -- 投稿内容
        """

        self.pub_date = pub_date
        self.name = name
        self.comment = comment


try:
    db.create_all()
except Exception as e:
    print(e.args)
    pass


@app.route('/')
def hello():
     # テーブルから投稿データをSELECT文で引っ張ってくる
    text = Comment.query.all()
    print(type(text))
    return render_template("index.html", lines=text)
#td preフォーマットで書くと良い


@app.route('/good')
def good():
    name = "Good"
    return name

@app.route('/post_data_old', methods=['POST'])
def checks():
    return request.json["text"]

@app.route('/post_data', methods=['POST'])
def check():
    date =datetime.now()
    comment =request.json["text"]
    name = request.json["name"]
     # テーブルに格納するデータを定義する
    comment_data = Comment(pub_date=date, name=name, comment=comment)
    # テーブルにINSERTする
    db.session.add(comment_data)
    # テーブルへの変更内容を保存
    db.session.commit()
    return request.json["text"]
        


## おまじない
if __name__ == "__main__":
    app.run(debug=True)
