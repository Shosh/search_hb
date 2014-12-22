import unittest
from spider import Spider


class TestSpider(unittest.TestCase):
    def setUp(self):
        self.test_spider = Spider("aladinfoods.bg")

    def test_spider_init(self):
        self.assertEqual(self.test_spider.scaned_url, [])
        self.assertEqual(self.test_spider.domain, "aladinfoods.bg")
        
    def test_is_outgoing(self):
        self.assertFalse(self.test_spider.is_outgoing("http://aladinfoods.bg"))

    def test_is_not_outgoing(self):
        self.assertTrue(self.test_spider.is_outgoing("http://hackbulgaria.com"))

    def test_is_valid(self):
        self.assertTrue(self.test_spider.is_valid("http://aladinfoods.bg/menu"))
        
    def test_is_not_valid(self):
        self.assertFalse(self.test_spider.is_valid("http://hackbulgaria.com"))
        
if __name__ == '__main__':
    unittest.main()
