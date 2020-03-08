import time
from selenium.webdriver.common.action_chains import ActionChains


class FeaturePage():

    def __init__(self, driver, feature_name):
        self.driver = driver
        for _ in range(100):
            if self.driver.find_element_by_class_name('header-section').text == feature_name:
                break
            time.sleep(0.1)
        else:
            raise Exception

        self.scroll_end_page()

    def get_all_comment_boxes(self):
        return self.driver.find_elements_by_class_name('comments-button-box')

    def click_comment_box(self, comment_box_element):
        action = ActionChains(self.driver)
        action.move_to_element(comment_box_element).perform()
        comment_box_element.click()

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
