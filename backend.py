from flask import Flask #Flask app

import bcrypt

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greeting():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)