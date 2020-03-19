from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random


class MainPage():

    def __init__(self, driver, driver_wait):
        self.driver = driver
        self.driver_wait = driver_wait
        self.driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="https://www.lovetoknow.com/"]')))

    def get_supernav_verticals(self):
        return self.driver_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'supernav-vertical')))

    def get_main_content(self):
        return self.driver_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'main')))

    def get_main_content_sections(self):
        return self.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'main > section')))

    def get_footer_element(self):
        return self.driver_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'footer')))

    def get_sections_from_footer_element(self):
        return self.get_footer_element()[0].find_elements_by_tag_name('section')

    def get_features_in_features_section(self):
        return self.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li.feature')))

    def get_features_section_from_main_content(self):
        return self.driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'section.features')))

    def click_random_article(self):
        random_number = random.randrange(len(self.get_features_in_features_section()))
        feature_name = self.get_features_in_features_section()[random_number].text.split('\n')[0]

        random_number2 = random.randrange(2)
        article = self.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ol.feature-content > li')))[random_number * 2 + random_number2]
        article_name = article.text
        print('Article name = %s' % article.text)
        article.click()

        return article_name, feature_name

    def get_articles_from_feature(self, feature_element):
        return feature_element.find_elements_by_tag_name('li')
