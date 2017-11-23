import threading
import unittest
import requests

from dmoj.control import JudgeControlRequestHandler

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from http.server import HTTPServer
except ImportError:
    from BaseHTTPServer import HTTPServer


class ControlServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class FakeJudge(object):
            pass

        class Handler(JudgeControlRequestHandler):
            judge = FakeJudge()

        cls.judge_class = FakeJudge
        cls.server = HTTPServer(('127.0.0.1', 0), Handler)

        thread = threading.Thread(target=cls.server.serve_forever)
        thread.daemon = True
        thread.start()

        cls.connect = 'http://%s:%s/' % cls.server.server_address

    def setUp(self):
        self.update_mock = self.judge_class.update_problems = mock.Mock()

    def test_get_404(self):
        self.assertEqual(requests.get(self.connect).status_code, 404)
        self.assertEqual(requests.get(self.connect + 'update/problems').status_code, 404)

    def test_update_problem(self):
        requests.post(self.connect + 'update/problems')
        self.update_mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
