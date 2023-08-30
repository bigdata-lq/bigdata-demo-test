import time
from selenium import webdriver
driver  =  webdriver.Chrome()
driver.get("http://www.baidu.com")
driver.find_element_by_css_selector("input[id=\"kw\"]").send_keys('selenium')  #定位输入框输入selenium
driver.find_element_by_css_selector("input[type=\"submit\"]").click() #定位搜索按钮点击按钮,属性选择type
time.sleep(5)
res=driver.find_element_by_id('1')   #获得搜索结果列表的第一项
print(res.text)
driver.quit()