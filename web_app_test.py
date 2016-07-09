from flask import Flask, render_template, request
import pymongo

# Flaskの宣言
app = Flask(__name__)

# mongoDBへの接続
client = pymongo.MongoClient("localhost", 27017)
db = client.my_mongo
collection = db.artist_data

title = "100本ノック課題69番"

@app.route('/')
def index():
    message = "アーティストの情報検索できるWebアプリケーション（直球）"
    return render_template("index.html", message=message, title=title)


@app.route("/post", methods=["GET", "POST"])
def post():
    message = "検索結果"
    cursor = collection.find({"name": "Queen"})
    if request.method == "POST":
        request_dict = dict(request.form)
        order = request_dict.pop("order")[0]
        number = int(request_dict.pop("number").pop().replace("件", ""))

        del_key_list = []

        for key, value in request_dict.items():
            if len(value) == 1 and value[0] == "":
                del_key_list.append(key)
            else:
                request_dict[key] = request_dict[key].pop()

        for key in del_key_list:
            del(request_dict[key])

        if order == "昇順":
            search_result = collection.find(request_dict).sort("rating.value", pymongo.ASCENDING).limit(number)
        else:  # 例外処理めんどいのでelseでなんとかする
            search_result = collection.find(request_dict).sort("rating.value", pymongo.DESCENDING).limit(number)

        return render_template("index.html", message=message, title=title, result=search_result)

if __name__ == '__main__':
    app.debug = True
    app.run()
