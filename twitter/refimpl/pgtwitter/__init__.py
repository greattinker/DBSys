# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''main app module, configuration etc.
The more interesting API implementation is imported at the very bottom'''

from flask import Flask

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

from pgwsdm.pool import ReplicatedPostgresConnectionPool

app = Flask(__name__)
app.debug = True


# pool = ReplicatedPostgresConnectionPool(maxsize=3, database="wsdm",
#                                         user="hduser",
#                                         masters=["141.76.47.226",
#                                                  "141.76.47.227",
#                                                  "141.76.47.228",
#                                                  "141.76.47.229",
#                                                  "141.76.47.230",
#                                                  "141.76.47.220",
#                                                  "141.76.47.221",
#                                                  "141.76.47.222",
#                                                  "141.76.47.223",
#                                                  "141.76.47.224"],
#                                         write_master="141.76.47.225")
pool = ReplicatedPostgresConnectionPool(maxsize=8, database="twitter",
                                        user="ebi",
                                        masters=["localhost"],
                                        write_master="localhost")

# import for side-effects (registering URL handlers)
import pgwsdm.read
import pgwsdm.write
import pgwsdm.imports

if __name__ == '__main__':
    app.run()
