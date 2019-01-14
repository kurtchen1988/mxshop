
dsn = 'http://eb19b9a37c984b4797911593bdbe445a:ec18477f960f462da328a7374a1ffbe5@127.0.0.1:9000/2'

from raven import Client

client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()