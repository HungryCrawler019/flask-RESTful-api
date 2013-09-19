import unittest
from flask import Flask
import flask_restful
from flask_restful.utils import cors
from nose.tools import assert_equals, assert_true


class CORSTestCase(unittest.TestCase):

    def test_crossdomain(self):

        class Foo(flask_restful.Resource):
            @cors.crossdomain(origin='*')
            def get(self):
                return "data"

        app = Flask(__name__)
        api = flask_restful.Api(app)
        api.add_resource(Foo, '/')

        with app.test_client() as client:
            res = client.get('/')
            assert_equals(res.status_code, 200)
            assert_equals(res.headers['Access-Control-Allow-Origin'], '*')
            assert_equals(res.headers['Access-Control-Allow-Methods'], 'HEAD, OPTIONS, GET')
            assert_equals(res.headers['Access-Control-Max-Age'], '21600')

    def test_no_crossdomain(self):

        class Foo(flask_restful.Resource):
            def get(self):
                return "data"

        app = Flask(__name__)
        api = flask_restful.Api(app)
        api.add_resource(Foo, '/')

        with app.test_client() as client:
            res = client.get('/')
            assert_equals(res.status_code, 200)
            assert_true('Access-Control-Allow-Origin' not in res.headers)
            assert_true('Access-Control-Allow-Methods' not in res.headers)
            assert_true('Access-Control-Max-Age' not in res.headers)
