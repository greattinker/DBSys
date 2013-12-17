import urllib2
import random
import time
import os
import base64
import json
import sys

NUM_USERS = None
URL_BASE = None

def parse_args():
    global NUM_USERS, URL_BASE
    if len(sys.argv) != 4:
        print >> sys.stderr, 'Pass size and url parameter, e.g. "multimech-run wldriver 100000 http://0.0.0.0:8000"'
        sys.exit()
    try:
        NUM_USERS = int(sys.argv[2])
        URL_BASE = sys.argv[3]
    except ValueError:
        print >> sys.stderr, 'Pass size and url parameter, e.g. "multimech-run wldriver 100000 http://0.0.0.0:8000"'
        sys.exit()

if NUM_USERS == None or URL_BASE == None:
    parse_args()


def random_message(length):
    return base64.urlsafe_b64encode(os.urandom(length))

class Transaction(object):
    def __init__(self):
        pass

    def run(self):
        username = "user_%i" % random.randint(0, NUM_USERS - 1)
        get_req = urllib2.Request(url=URL_BASE + '/tweets',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"username": username}))

        start_timer = time.time()
        resp = urllib2.urlopen(get_req)
        resp.read()
        latency = time.time() - start_timer
        self.custom_timers['get_tweets'] = latency
        assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.code


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
