
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

db = SQLAlchemy(app)    #SQL alchemy database instance


if __name__ == '__main__':
    app.run(debug=True)


