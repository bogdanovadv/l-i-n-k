from flask import Flask, jsonify, request, redirect
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import pymysql
from config import Config
from flask_cors import CORS
import hashlib
import base64


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine(f'mysql+pymysql://{Config.db_user}:{Config.db_pass}@{Config.db_host}/{Config.db_name}')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


from models import *


jwt = JWTManager(app)

cors = CORS(app, resources={
    r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}
})




# Создаем таблицы в БД
# Раскоментируй строчку ниже, если нужно первоначальное создание таблиц
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.route('/register', methods=['POST'])
def register():
    print('sdasd')
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    print('qqq', user.name)
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token, 'name': user.name}


def add_original_link(original_link):
    links = Original.query.filter(Original.link ==original_link).first()
    if not links:
        new_original_link = {'link': original_link}
        add_new_original_link = Original(**new_original_link)
        session.add(add_new_original_link)
        session.commit()
        links = Original.query.filter(Original.link == original_link).first()
    return links

@app.route('/add-link', methods=['POST'])
@jwt_required()
def add_link():
    user_id = get_jwt_identity()
    response_data = request.json
    original_link = add_original_link(response_data["original"])
    exist = Link.query.filter(Link.original_id == original_link.id).first()
    if not exist:
        response_data.pop("original")
        response_data["original_id"] = original_link.id
        new_one = Link(**response_data)
        new_one.user_id = user_id

        new_one.short_link = base64.urlsafe_b64encode(hashlib.md5(original_link.link.encode("UTF-8")).digest()).decode()[:12]

        new_one.counter = 0
        session.add(new_one)
        session.commit()
        serialized = {
            'original': original_link.link,
            'short_link': f"{Config.api_url}/{new_one.short_link}",
            'type_id': new_one.type_id,
            'counter': new_one.counter,
            "user_id": user_id
        }
        if new_one.friendly_link:
            serialized["friendly"] = new_one.friendly_link
    else:
        serialized = {
            'message': "Запись уже существует"
        }

    return jsonify(serialized)


@app.route('/links', methods=['GET'])
@jwt_required()
def get_list():
    user_id = get_jwt_identity()
    links = Link.query.filter(Link.user_id == user_id)
    serialized = []
    for link in links:
        data = {
            'id': link.id,
            'original': link.original.link,
            'short': f"{Config.api_url}/{link.short_link}",
            'counter': link.counter,
            'type_id': link.type_id
        }
        if link.friendly_link:
            friendly_link = f"{Config.api_url}/{link.friendly_link}"
            data['friendly'] = friendly_link
        serialized.append(data)
    return jsonify(serialized)


@app.route('/links/<int:link_id>', methods=['PUT'])
@jwt_required()
def update_link(link_id):
    user_id = get_jwt_identity()
    item = Link.query.filter(Link.id == link_id, Link.user_id == user_id).first()
    params = request.json
    if not item:
        return {'message': 'Нет ссылок с таким id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'type_id': item.type_id,
        'friendly': item.friendly_link
    }
    return serialized


@app.route('/links/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_link(link_id):
    user_id = get_jwt_identity()
    item = Link.query.filter(Link.id == link_id, Link.user_id == user_id).first()
    if not item:
        return {'message': 'Нет ссылок с таким id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/<short_uri>')
def url_redirect(short_uri):
    link = Link.query.filter(Link.short_link == short_uri).first()
    # print(link.original.link)
    if not link:
        link = Link.query.filter(Link.friendly_link == short_uri).first()
    if link:
        if link.type_id == 1:
            link.counter += 1
            session.commit()
            return redirect(link.original.link)
        elif link.type_id == 2:
            if check_autentificate():
                link.counter += 1
                session.commit()
                return redirect(link.original.link)
        else:
            if check_private_link(link.user_id):
                link.counter += 1
                session.commit()
                return redirect(link.original.link)
            else:
                return {'message': 'Недостаточно прав'}, 400
    else:
        return {'message': 'Ссылка недействительна'}, 400


@jwt_required()
def check_autentificate():
    return get_jwt_identity()


@jwt_required()
def check_private_link(link_user_id):
    user_id = get_jwt_identity()
    if user_id == link_user_id:
        return True


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(host=Config.api_host, port=Config.api_port)
