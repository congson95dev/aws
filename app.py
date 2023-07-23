from flask import Flask
from s3_upload import s3_bp

app = Flask(__name__)
app.register_blueprint(s3_bp)

if __name__ == '__main__':
    app.run(debug=True)