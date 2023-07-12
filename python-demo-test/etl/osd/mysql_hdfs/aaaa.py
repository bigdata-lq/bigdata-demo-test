class TestLogin(object):

    def __init__(self):
        pass

    def test_login1(self):
        print(11)
        assert 1

    def test_login2(self):
        assert 1

    def test_login3(self):
        assert 0


# 1)先执行pytest  再执行命令 allure generate report/ -o report/html

# aaaaa = TestLogin()
print(TestLogin().test_login1())