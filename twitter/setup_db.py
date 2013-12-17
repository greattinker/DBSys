'''data generator that speaks to the import part of the API
documentation at the bottom.'''
import random
import urllib2
import json
import base64
import os
import sys
from datetime import datetime, timedelta
import time
import multiprocessing
import argparse

URL_BASE = None
NUM_USERS = None

FRIENDS_MU = 80
FRIENDS_SIGMA = 40
TWEETS_MU = 200
TWEETS_SIGMA = 100
LAST_BASE_TWEET = datetime.strptime("2012-10-29", "%Y-%m-%d")


def random_message(length):
    return base64.urlsafe_b64encode(os.urandom(length))


def _create_user(i):
    username = "user_%i" % i
    password = "pass_%i" % i
    req = urllib2.Request(url=URL_BASE + '/create_user',
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps(
                              {
                                  "username": username,
                                  "password": password
                              }))
    try:
        resp = urllib2.urlopen(req)
        resp.read()
    except Exception, e:
        print >> sys.stderr, e
        sys.exit()


def prepare_users():
    workload = range(NUM_USERS)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    p = pool.map_async(_create_user, workload)
    try:
        p.get(0xFFFF)
    except KeyboardInterrupt:
        print 'parent received control-c'


def _create_friendships(i):
    username = "user_%i" % i

    num_friends = int(random.gauss(FRIENDS_MU, FRIENDS_SIGMA))
    if num_friends < 0:
        num_friends = 0
    if num_friends > NUM_USERS:
        num_friends = NUM_USERS

    friends = random.sample(xrange(NUM_USERS), num_friends)
    if i not in friends:
        friends.append(i)

    req = urllib2.Request(url=URL_BASE + '/import_friends',
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps({
                              "username": username,
                              "friends": ["user_%i" % f for f in friends]
                          }))
    try:
        resp = urllib2.urlopen(req)
        resp.read()
    except Exception, e:
        print >> sys.stderr, e
        sys.exit()


def prepare_follows():
    workload = range(NUM_USERS)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    p = pool.map_async(_create_friendships, workload)
    try:
        p.get(0xFFFF)
    except KeyboardInterrupt:
        print 'parent received control-c'


def rand_date_in_last_year():
    now = datetime.now()
    last_year = now - timedelta(days=365)
    return random.randrange(time.mktime(last_year.timetuple()),
                            time.mktime(now.timetuple()))


def _create_tweets(i):
    username = "user_%i" % i

    num_tweets = int(random.gauss(TWEETS_MU, TWEETS_SIGMA))
    if num_tweets < 0:
        num_tweets = 0

    tweets = [random_message(random.randint(10, 140)) for _ in xrange(num_tweets)]
    timestamps = [rand_date_in_last_year() for _ in tweets]

    req = urllib2.Request(url=URL_BASE + '/import_tweets',
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps(
                              {
                                  "username": username,
                                  "bodies": tweets,
                                  "timestamps": timestamps
                              }))
    try:
        resp = urllib2.urlopen(req)
        resp.read()
    except Exception, e:
        print >> sys.stderr, e
        sys.exit()


def prepare_tweets():
    workload = range(NUM_USERS)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    p = pool.map_async(_create_tweets, workload)
    try:
        p.get(0xFFFF)
    except KeyboardInterrupt:
        print 'parent received control-c'

# def clear_tweets():
#     req = urllib2.Request(url=URL_BASE + '/delete_tweets_after',
#         headers={'Content-Type': 'application/json'},
#         data=json.dumps(
#             {
#                 "delete_after": time.mktime(LAST_BASE_TWEET.timetuple()),
#             }))
#     resp = urllib2.urlopen(req)
#     resp.read()
#     return


class HelpfulParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)

if __name__ == '__main__':
    parser = HelpfulParser(description='Creates the wsdm exercise database')
    parser.add_argument('-H', '--host', help='host of your application e.g. 0.0.0.0 or localhost', required=False, default="0.0.0.0")
    parser.add_argument('-p', '--port', help='port your application is running on e.g. 8000', type=int, required=False, default=8001)
    parser.add_argument('-s', '--database_size', help='size of the test database in users', type=int, required=False, default=1000000)
    parser.add_argument('task', help='task to run [load_users, load_follows, load_tweets]')

    args = parser.parse_args()

    task = {
        "load_users": prepare_users,
        "load_follows": prepare_follows,
        "load_tweets": prepare_tweets,
        # "clear_tweets": clear_tweets
    }.get(args.task)

    NUM_USERS = args.database_size
    URL_BASE = "http://%s:%i" % (args.host, args.port)
    start_time = time.time()
    task()
    print "finished in ", time.time() - start_time
