from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '這是第二次測試'

if __name__ == '__main__':
    app.run()
