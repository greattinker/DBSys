'''Two implementations of the write api (normalized/denormalized)'''
import json
from flask import request, Response
from pgwsdm import app, pool


# @app.route('/post_tweet', methods=['POST'])
@app.route('/post_tweet_normal', methods=['POST'])
def post_tweet():
    '''simple insert into one normalized table'''
    data = json.loads(request.data)
    username, body = data['username'], data['body']

    with pool.write_cursor() as c:
        c.execute(
            """insert into tweets("user", body)
                select id, %s from users where username = %s""",
            (body, username))
    return Response(status=200)


# @app.route('/post_tweet_dn', methods=['POST'])
@app.route('/post_tweet', methods=['POST'])
def post_tweet_dn():
    '''for the denormalized case, a complex transaction spanning mutliple user
    rows has to be performed'''
    data = json.loads(request.data)
    username, body = data['username'], data['body']

    with pool.write_cursor() as c:
        c.execute(
            """
            start transaction;
            with inserted_ids AS (
                insert into tweets("user", body)
                    select id, %s from users where username = %s
                returning *
            )
            update users set stream = stream || (select id from inserted_ids)
            where users.id in (
                select follows from following where "user" = (select "user" from inserted_ids)
            );
            commit;""",
            (body, username))
    return Response(status=200)


@app.route('/add_friend', methods=['POST'])
def add_friend():
    data = json.loads(request.data)
    username = data['username']
    friend = data['friend']
    with pool.write_cursor() as c:
        c.execute(
            """insert into following
            select u.id, followers.id from users u, users followers
            where u.username = %s
            and followers.username = %s""",
            (username, friend))

    return Response(status=200)


@app.route('/create_user', methods=['POST'])
def create_user():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']

    with pool.write_cursor() as c:
        c.execute(
            "insert into users(username, password) values(%s, %s)", (username, password))

    return Response(status=200)
