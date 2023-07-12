import unittest

class TestMethods(unittest.TestCase):
    # 通过测试
    def test_pass(self):
        self.assertEqual(1+1,2)

    # 没通过测试
    def test_failed(self):
        self.assertEqual(1 - 1, 2)

    # 报错
    def test_error(self):
        self.assertEqual(1 - 2, num)

if __name__ == '__main__':
    unittest.main()
