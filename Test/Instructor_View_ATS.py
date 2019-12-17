import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MavLearn_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_mavlearning(self):
        user = "instructor"
        pwd = "maverick1a"
        driver = self.driver
        heroku_site = "https://mavlearning.herokuapp.com"
        local_site = "http://127.0.0.1:8000"
        driver.get(heroku_site)
        # Instructor Login
        elem = driver.find_element_by_xpath('//*[@id="header"]/ul/li/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_username"]')
        elem.send_keys(user)
        elem = driver.find_element_by_xpath('//*[@id="id_password"]')
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        # Instructor Create Course
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/p[2]/a[1]')
        time.sleep(5)
        elem.click()
        time.sleep(2)
        elem = driver.find_element_by_xpath('//*[@id="id_subject"]/option[3]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_title"]')
        elem.send_keys("Python")
        elem = driver.find_element_by_xpath('//*[@id="id_slug"]')
        elem.send_keys("python")
        elem = driver.find_element_by_xpath('//*[@id="id_overview"]')
        elem.send_keys("This is a course about Python")
        time.sleep(5)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/p[5]/input')
        elem.click()
        # Create Modules in course
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[3]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_modules-0-title"]')
        elem.send_keys("Python 101")
        elem = driver.find_element_by_xpath('//*[@id="id_modules-0-description"]')
        elem.send_keys("Python Part 1")
        elem = driver.find_element_by_xpath('//*[@id="id_modules-1-title"]')
        elem.send_keys("Python 102")
        elem = driver.find_element_by_xpath('//*[@id="id_modules-1-description"]')
        elem.send_keys("Python Part 2")
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/input[18]')
        elem.click()
        time.sleep(5)
        # Create Quiz
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/p/a[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/p[2]/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_name"]')
        elem.send_keys("Python Quiz")
        elem = driver.find_element_by_xpath('//*[@id="id_description"]')
        elem.send_keys("First Python Quiz")
        elem = driver.find_element_by_xpath('//*[@id="id_roll_out"]')
        elem.click()
        time.sleep(2)
        # Add Questions to quiz
        question1 = "What is the output function used in python?"
        question2 = "(True or False) [ ] represents an Array list."
        q1a1 = "print()"
        q1a2 = "I don't know"
        q2a1 = "True"
        q2a2 = "False"
        elem = driver.find_element_by_xpath('//*[@id="id_questions_for-0-label"]')
        elem.send_keys(question1)
        elem = driver.find_element_by_xpath('//*[@id="id_questions_for-1-label"]')
        elem.send_keys(question2)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/p[4]/input')
        time.sleep(3)
        elem.click()
        # Create Answers for quiz
        # Add 2 answers for question 1
        time.sleep(3)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_question"]/option[4]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_text"]')
        elem.send_keys(q1a1)
        elem = driver.find_element_by_xpath('//*[@id="id_is_correct"]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="module"]/form/input[2]')
        time.sleep(2)
        elem.click()
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_question"]/option[4]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_text"]')
        elem.send_keys(q1a2)
        elem = driver.find_element_by_xpath('//*[@id="module"]/form/input[2]')
        time.sleep(2)
        elem.click()
        # Add 2 answers for question 2
        time.sleep(2)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_question"]/option[5]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_text"]')
        elem.send_keys(q2a1)
        elem = driver.find_element_by_xpath('//*[@id="id_is_correct"]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="module"]/form/input[2]')
        time.sleep(5)
        elem.click()
        time.sleep(2)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_question"]/option[5]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_text"]')
        elem.send_keys(q2a2)
        elem = driver.find_element_by_xpath('//*[@id="module"]/form/input[2]')
        time.sleep(5)
        elem.click()
        # Add Module Content (text, video, and quiz)
        time.sleep(2)
        # Create text content
        elem = driver.find_element_by_xpath('//*[@id="header"]/a')
        elem.click()
        text = "Welcome to Python 101!"
        text1 = "This is the first post about Python"
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[4]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul/li[1]/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_title"]')
        elem.send_keys(text)
        elem = driver.find_element_by_xpath('//*[@id="id_content"]')
        elem.send_keys(text1)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/p[3]/input')
        time.sleep(2)
        elem.click()
        # Create video content
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul/li[3]/a')
        elem.click()
        video = "https://www.youtube.com/watch?v=qwdjCh3e4TY"
        video_title = "Python for beginners"
        elem = driver.find_element_by_xpath('//*[@id="id_title"]')
        elem.send_keys(video_title)
        elem = driver.find_element_by_xpath('//*[@id="id_url"]')
        elem.send_keys(video)
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/p[3]/input')
        time.sleep(3)
        elem.click()
        # Create quiz content
        elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul/li[5]/a')
        elem.click()
        quiz_title = "Python Quiz 1"
        time.sleep(2)
        elem = driver.find_element_by_xpath('//*[@id="id_title"]')
        elem.send_keys(quiz_title)
        elem = driver.find_element_by_xpath('//*[@id="id_course"]/option[2]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_module"]/option[3]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="id_quiz"]/option[3]')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/form/p[5]/input')
        time.sleep(2)
        elem.click()
        time.sleep(2)
        # Delete Course
        elem = driver.find_element_by_xpath('//*[@id="header"]/a')
        elem.click()
        elem = driver.find_element_by_xpath('//*[@id="content"]/div/div/p/a[2]')
        elem.click()
        # Sign Out
        elem = driver.find_element_by_xpath('//*[@id="header"]/ul/li/a')
        elem.click()
        time.sleep(5)



        def tearDown(self):
            self.driver.close()

    if __name__ == "__main__":
        unittest.main()
