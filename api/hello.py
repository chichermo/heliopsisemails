from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "¡Hola Mundo! Vercel funciona!"

handler = app
