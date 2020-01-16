import unittest
from app import app, process1, process2, process3


class TestViews(unittest.TestCase):
    def setUp(self):
        self.logger = app.logger
        app.testing = True
        self.client = app.test_client()

    def test_any_methods_request(self):
        with self.assertLogs(self.logger, level='ERROR') as log:
            result = self.client.post('/api')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Error. Method Not Allowed.', result.data)
        self.assertListEqual(log.output, [
            "ERROR:app:Method: POST. Message: Error, method not allowed. Url: http://localhost/api. Data: b''"])

    def test_any_path_view(self):
        with self.assertLogs(self.logger, level='ERROR') as log:
            result = self.client.get('/api/any_path')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Error. Wrong path.', result.data)
        self.assertListEqual(log.output, ["ERROR:app:Method: GET. Url: http://localhost/api/any_path. Data: b''"])

    def test_api_view(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'ok', result.data)
        self.assertListEqual(log.output, ["INFO:app:Method: GET. Url: http://localhost/api. Data: b''",
                                          'INFO:app:Process1 started', 'INFO:app:Process2 started',
                                          'INFO:app:Process3 started'])

    def test_api_view_invalid(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api?invalid=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Error. Parameter invalid = 1.', result.data)
        self.assertListEqual(log.output, ["INFO:app:Method: GET. Url: http://localhost/api?invalid=1. Data: b''",
                                          'ERROR:app:Message: Error. Parameter invalid = 1.'])

    def test_api_view_notawaiting(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            result = self.client.get('/api?notawaiting=1')
            self.assertEqual(200, result.status_code)
            self.assertEqual(b'Error. Parameter notawaiting = 1.', result.data)
        self.assertListEqual(log.output, ["INFO:app:Method: GET. Url: http://localhost/api?notawaiting=1. Data: b''",
                                          'INFO:app:Process1 started', 'INFO:app:Process2 started',
                                          'ERROR:app:Message: Error. Parameter notawaiting = 1.'])


class TestProcessX(unittest.TestCase):
    def setUp(self):
        self.logger = app.logger

    def test_process1(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            process1(None)
        self.assertListEqual(log.output, ['INFO:app:Process1 started'])

    def test_process2(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            with self.assertRaises(Exception) as e:
                process2({'notawaiting': '1'})
            self.assertEqual(e.exception.__str__(), 'Error. Parameter notawaiting = 1.')
        self.assertListEqual(log.output, ['INFO:app:Process2 started'])

        with self.assertLogs(self.logger, level='INFO') as log:
            process2({'notawaiting': '0'})
        self.assertListEqual(log.output, ['INFO:app:Process2 started'])

    def test_process3(self):
        with self.assertLogs(self.logger, level='INFO') as log:
            process3(None)
        self.assertListEqual(log.output, ['INFO:app:Process3 started'])


if __name__ == "__main__":
    unittest.main()
