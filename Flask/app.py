from kusto import get_data2
from flask import Flask, jsonify


app = Flask(__name__)

@app.route("/data")
def data():
    results = get_data2()
    # return jsonify(results)
    return results

@app.route("/hello")
def hello():
    hello = "<h1>Hello World</h1>"
    return jsonify(hello)

if __name__ == "__main__":
    app.run(debug=True)