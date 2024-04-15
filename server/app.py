#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):

    def get(self):
        _id = session.get('user_id')
        if _id:
            user = User.query.filter(User.id == _id).first()
            return make_response(user.to_dict(), 200)
        else:
            return {}, 204

class Login(Resource):
    
    def post(self):
        user = User.query.filter(User.username == request.get_json()['username']).first()
        session['user_id'] = user.id
        return user.to_dict(), 200

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
