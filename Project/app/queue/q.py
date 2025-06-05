from redis import Redis
from rq import Queue


# "valkey" host to localhost
radis_connection = Redis(
    host="localhost",
    port=6379
)

q = Queue(connection=radis_connection)