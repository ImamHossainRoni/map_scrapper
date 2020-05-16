from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/data/", methods=['GET'])
def get_data():
    city = request.args.get('city')
    keyword = request.args.get('keyword')
    country = request.args.get('country')
    import scrapper_code as sc
    sc.run(city=city, country=country, keyword=keyword)
    return "Still scrapping is running and saving data to file!"


if __name__ == "__main__":
    app.run(debug=True)
