from django.test import TestCase
from custom_admin.admin import CustomAdminSite


class CustomAdminTest(TestCase):

    def setUp(self):
        self.site = CustomAdminSite()

    def test_get_filter_info(self):
        post1 = {
            'filter': '{"active":"1","platform_type__id__exact":"4"}'
        }
        res1 = {'active': '1', 'platform_type__id__exact': '4'}

        filter_info1 = self.site.get_filter_info(post1)
        self.assertEqual(res1, filter_info1)

        post2 = {
            'filter': '{"a" : "1", "b" : "2", "c": "3"}'
        }
        res2 = {'a': '1', 'b': '2', 'c': '3'}
        filter_info2 = self.site.get_filter_info(post2)
        self.assertEqual(res2, filter_info2)

    def test_get_filter_dict(self):
        key = 'key'
        value = 'value'
        filter_dict = self.site.get_filter_dict(key, value)
        res = {'key': 'value'}
        self.assertEqual(filter_dict, res)

        key = 'key'
        value = '++%2B%2B++'
        filter_dict = self.site.get_filter_dict(key, value)
        res = {'key': '  ++  '}
        self.assertEqual(filter_dict, res)
