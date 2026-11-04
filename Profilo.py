from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Studio Medico d'Élite - Online!"

if __name__ == '__main__':
    app.run()
