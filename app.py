import typing

import boto3
from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import typesystem


class Limit(typesystem.Integer):
    description = 'The minimum (1) and maximum (10) number of buckets allowed to be returned.'
    minimum = 1
    maximum = 10


def list_buckets(limit: Limit) -> typing.List[str]:
    s3 = boto3.resource('s3')
    return [bucket.name for bucket in s3.buckets.limit(limit)]


routes = [
    Route('/buckets', 'GET', list_buckets),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)

if __name__ == '__main__':
    app.main()
