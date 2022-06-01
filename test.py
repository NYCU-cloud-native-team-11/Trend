import main
import unittest
import sys


class TestStringMethods(unittest.TestCase):
    def test_get_input(self):
        self.assertEqual(main.get_input(['main.py', 'TSMC']), ['TSMC'])

    def test_get_input_error(self):
        with self.assertRaises(SystemExit) as cm:
            main.get_input(['TSMC'])
        self.assertEqual(cm.exception.code, 1)

    def test_upload_data_wrong_url(self):
        wrong_url = 'https://cloud-11-backend.herokuapp.com/api/trend/'
        list_key = main.get_input(['main.py', 'TSMC'])
        json_list = main.get_trend(list_key)
        self.assertEqual(str(main.upload_data(
            wrong_url, json_list)), "<Response [404]>")

    def test_upload_data_right_url(self):
        right_url = 'https://cloud-11-backend.herokuapp.com/api/trends/'
        list_key = main.get_input(['main.py', 'TSMC'])
        json_list = main.get_trend(list_key)
        self.assertEqual(str(main.upload_data(
            right_url, json_list)), '<Response [200]>')

    def test_get_trend(self):
        self.assertEqual(main.get_trend(
            ['TSMC']), '{"company": "TSMC", "count": 14, "date": "2022-05-29"}')


if __name__ == '__main__':
    unittest.main()
