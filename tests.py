from apistar.test import TestClient
import app
from moto import mock_s3
import boto3


@mock_s3
def test_list_buckets_directly_with_valid_limits():
    create_buckets()

    buckets = app.list_buckets(3)
    assert len(buckets) == 2

    buckets = app.list_buckets(2)
    assert len(buckets) == 2

    buckets = app.list_buckets(1)
    assert len(buckets) == 1


@mock_s3
def test_list_buckets_with_client_valid_limit():
    create_buckets()

    client = TestClient(app.app)
    response = client.get('http://localhost/buckets?limit=1')

    assert response.status_code == 200
    assert response.json() == ['resources.influentialcode.com'] or response.json == ['testing.influentialcode.com']


@mock_s3
def test_list_buckets_with_client_invalid_limit():
    create_buckets()

    client = TestClient(app.app)
    response = client.get('http://localhost/buckets?limit=50')

    assert response.status_code == 400


@mock_s3
def create_buckets():
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket='resources.influentialcode.com')
    s3.create_bucket(Bucket='testing.influentialcode.com')


