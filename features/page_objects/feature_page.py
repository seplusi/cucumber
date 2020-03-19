import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import string


class FeaturePage:

    def __init__(self, driver, driver_wait, feature_name, article_name):
        self.driver = driver
        self.driver_wait = driver_wait
        self.feature_name = feature_name
        self.article_name = article_name

    def write_comment(self):
        comment = 'Test_%s' % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.textarea'))).send_keys(
            comment)
        self.driver_wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button.btn.post-action__button.full-size-button'))).click()

        return comment

    def login_using_disqus(self):
        self.driver.find_element_by_class_name("dropdown-toggle-wrapper").click()
        self.driver.find_elements_by_css_selector('ul.dropdown-menu > li')[0].click()

    def verify_headers(self):
        header_text = self.driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'header-section'))).text
        content_text = self.driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'header.content-header > h1'))).text

        return (header_text, content_text)

    def get_all_comment_boxes(self):
#        return self.driver.find_elements_by_class_name('comments-button-box')
        return self.driver_wait.until(EC.visibility_of_element_located(By.CLASS_NAME, 'comments-button-box'))

    def click_first_comment_box(self):
        comment_box = self.driver_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'comments-button-box')))[0]
        action = ActionChains(self.driver)
        action.move_to_element(comment_box).perform()
        comment_box.click()

    def scroll_end_page(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
