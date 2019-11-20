from flask import Flask, render_template, url_for, request, redirect
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ethquery import exec_query
import json

#initialize Flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Set api for restful access
api = Api(app)

class UserQuery(db.Model):
    '''
    User query class for restful api.
    '''
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, default=0)
    result = db.Column(db.String(200), default="")
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Query %r by %s on %s> %s' % (self.id, self.user, self.date_submitted, self.content)


@app.route('/', methods=['POST', 'GET'])
def index():
    '''
    response for "GET" and "POST" command on index page
    :return:
    '''
    if request.method=='POST':
        query_content = request.form['content']
        query_account = request.form['address']
        new_query = UserQuery(user=query_account,content=query_content)
        try:
            db.session.add(new_query)
            db.session.commit()
            '''
            Add the ethereum query below
            '''
            print(query_account,query_content)
            status, result = exec_query(query_account.strip(), query_content)
            new_query.result = result
            new_query.status = status
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        queries = UserQuery.query.order_by(UserQuery.date_submitted.desc()).all()
        return render_template('index.html', queries=queries)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    '''
    delete item with input id
    :param id: db record id
    :return: redirect or error info
    '''
    query_to_delete = UserQuery.query.get_or_404(id)
    try:
        db.session.delete(query_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting your query record'

parser = reqparse.RequestParser()
parser.add_argument('address')
parser.add_argument('content')

# API for RESTful access
class UserQueryApiGroup(Resource):
    def get(self):
        '''
        get method for restful request
        :return: query output in string
        '''
        queries = UserQuery.query.order_by(UserQuery.date_submitted.desc()).all()
        return str(queries)

    def post(self):
        '''
        post method for restful request
        :return: query output or error info in string
        '''
        args = parser.parse_args()
        user=args['address']
        content=args['content']
        if len(user) == 0 or len(content) == 0:
            return 'There was an issue parsing your request', 422
        new_query = UserQuery(user=user,content=content)
        try:
            db.session.add(new_query)
            db.session.commit()
            '''
            Add the ethereum query below
            '''
            print(query_account,query_content)
            status, result = exec_query(query_account.strip(), query_content)
            new_query.result = result
            new_query.status = status
            db.session.commit()
        except:
            return 'There was an issue adding your query'
        return str(new_query), 201

class UserQueryApiSingle(Resource):
    def get(self, id):
        '''
        check db data with query command
        :param id: db id
        :return: output in string
        '''
        query = UserQuery.query.get_or_404(id) 
        return str(query)

    def delete(self, id):
        '''
        delete db data with query command
        :param id: db id
        :return: output in string or error message
        '''
        query = UserQuery.query.get_or_404(id) 
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            return "Item could not be deleted", 404
        return "Item has been deleted", 204


api.add_resource(UserQueryApiSingle, '/api/<string:id>')
api.add_resource(UserQueryApiGroup, '/api')

if __name__ == "__main__":
    app.run(debug=True)
