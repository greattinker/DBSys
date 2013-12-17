'''Implementation of the bulk import api'''
from datetime import datetime
import json
from flask import request, Response
from pgwsdm import app, pool


# @app.route('/import_tweets', methods=['POST'])
@app.route('/import_tweets_n', methods=['POST'])
def import_tweets():
    data = json.loads(request.data)
    username, bodies = data['username'], data['bodies']
    timestamps = [datetime.fromtimestamp(c) for c in data['timestamps']]

    with pool.cursor() as c:
        c.executemany(
            """insert into tweets("user", created, body)
                    select id, %s, %s from users where username = %s""",
            [(t, b, username) for b, t in zip(bodies, timestamps)])
    return Response(status=200)


# @app.route('/import_tweets_dn', methods=['POST'])
@app.route('/import_tweets', methods=['POST'])
def import_tweets_dn():
    data = json.loads(request.data)
    username, bodies = data['username'], data['bodies']
    timestamps = [datetime.fromtimestamp(c) for c in data['timestamps']]

    with pool.cursor() as c:
        c.executemany(
            """
            start transaction;
            with insertion AS (
                insert into tweets("user", created, body)
                    select id, %s, %s from users where username = %s
                returning *
            )
            update users set stream = stream || (select id from insertion)
            where users.id in (select "user" from following where follows=(select "user" from insertion));
            commit;""",
            [(t, b, username) for b, t in zip(bodies, timestamps)])
    return Response(status=200)


@app.route('/import_friends', methods=['POST'])
def import_friends():
    data = json.loads(request.data)
    username = data['username']
    friends = data['friends']
    with pool.cursor() as c:
        c.execute(
            """insert into following
            select u.id, followers.id from users u, users followers
            where u.username = %s
            and followers.username in %s""",
            (username, tuple(friends)))

    return Response(status=200)
