from flask import Flask, make_response

app = Flask(__name__)


@app.route("/fall22", methods=['GET'])
def fall():
    with open('fall22_courses.json', 'r') as f:
        d = f.read()
        resp = make_response(d)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route("/winter23", methods=['GET'])
def winter():
    with open('winter23_courses.json', 'r') as f:
        d = f.read()
        resp = make_response(d)
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
