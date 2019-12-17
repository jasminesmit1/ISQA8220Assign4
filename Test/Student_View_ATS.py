import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class MavLearn_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_student_enroll(self):
        user = "groyce"
        pwd = "maverick1a"
        driver = self.driver
        heroku_site = "https://mavlearning.herokuapp.com"
        local_site = "http://127.0.0.1:8000"
        driver.get(heroku_site)
        # Student Register
        elem = driver.find_element_by_link_text("Django")
        elem.click()
        elem = driver.find_element_by_link_text("Register to enroll")
        elem.click()
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password1")
        elem.send_keys(pwd)
        elem = driver.find_element_by_id("id_password2")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/p/a')
        elem.click()
        elem = driver.find_element_by_xpath('///*[@id="content"]/div[2]/h3[2]/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/input[3]')
        elem.click()
        # view course detail
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/iframe')
        elem.click()
        time.sleep(5)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/iframe')
        elem.click()
        # Take Quiz
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="select"]/option[1]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="select"]/option[4]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/input')
        elem.click()
        time.sleep(3)
        elem = driver.find_element_by_xpath('//*[@id="content"]/label/a')
        elem.click()
        driver.get("http://127.0.0.1:8000")
        assert "Logged In"
        time.sleep(5)
        elem = driver.find_element_by_xpath("/html/body/div[1]/a/span").click()
        time.sleep(5)
        elem = driver.find_element_by_id("id_title")
        elem.send_keys("This is a test post with selenium")
        elem = driver.find_element_by_id("id_text")
        elem.send_keys("This is a test post of text with selenium")
        time.sleep(5)

        def tearDown(self):
            self.driver.close()

    if __name__ == "__main__":
        unittest.main()
