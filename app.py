from flask import Flask
from kenesis import kenesis_bp

app = Flask(__name__)
app.register_blueprint(kenesis_bp)

if __name__ == '__main__':
    app.run(debug=True)