'''Two implementations of the read api (normalized/denormalized and small variations)'''
import json
from flask import request, jsonify
from pgwsdm import app, pool


# @app.route('/tweets_r', methods=['POST'])
@app.route('/tweets', methods=['POST'])
def tweets_r():
    '''Fully relational implementation of the main test query'''
    data = json.loads(request.data)
    username = data['username']
    start = data.get("start", 0)
    limit = data.get("limit", 40)

    with pool.cursor() as c:
        c.execute(
            """select t.created, followers.username, t.body
                from users as u
                join following as f on u.id=f."user"
                join users as followers on f.follows=followers.id
                join tweets as t on t."user"=followers.id
                where u.username = %s
                order by t.created desc limit %s offset %s""", (username, limit, start))
        tweets = [list(row) for row in c.fetchall()]
    return jsonify({"tweets": tweets})


@app.route('/tweets_2q', methods=['POST'])
def tweets_2q():
    '''Performing some of the work in the application layer'''
    data = json.loads(request.data)
    username = data['username']
    start = data.get("start", 0)
    limit = data.get("limit", 40)

    with pool.cursor() as c:
        c.execute("""select fu.id, fu.username
            from users u, following f, users fu
            where
                u.username=%s and
                u.id=f."user" and
                f.follows=fu.id;""", (username, ))
        follows = dict(c.fetchall())
        # print tuple(follows.keys())
        c.execute("""select t.user, t.created, t.body
                    from tweets t
                    where t.user in %s
                    order by t.created limit %s offset %s""", (tuple(follows.keys()), limit, start))
        tweets = [list(row) for row in c.fetchall()]
    return jsonify({"tweets": tweets})


@app.route('/tweets_dn', methods=['POST'])
def tweets_dn():
    '''Querying the denormalized version of the db, in which each user tuple
    has a NF^2 "stream" attribute that contains all tweet-ids the user is
    interested in. Saves joins by performing more work at insert-time.'''
    data = json.loads(request.data)
    username = data['username']
    start = data.get("start", 0)
    limit = data.get("limit", 40)

    with pool.cursor() as c:
        c.execute("""select t.created, followers.username, t.body
                    from tweets as t,
                    users as followers,
                    (select
                        stream[array_upper(stream, 1)-%s:array_upper(stream, 1)-%s] as stream_tail
                        from users where username=%s) as s
                    where t.id = any(stream_tail)
                    and followers.id=t."user"
                    order by t.created desc""", (limit + start - 1, start, username))
        tweets = [list(row) for row in c.fetchall()]
    return jsonify({"tweets": tweets})


@app.route('/tweets_f', methods=['POST'])
# @app.route('/tweets', methods=['POST'])
def tweets_f():
    '''Keeping the business logic in the database.'''
    data = json.loads(request.data)
    username = data['username']
    start = data.get("start", 0)
    limit = data.get("limit", 40)

    with pool.cursor() as c:
        c.execute("select * from tweets_dn(%s, %s, %s);", (username, limit, start))
        tweets = [list(row) for row in c.fetchall()]
    return jsonify({"tweets": tweets})
