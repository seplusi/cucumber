class MainPage():

    def __init__(self, driver):
        self.driver = driver
        self.navbar_header = self.driver.find_element_by_class_name('navbar-header')
        self.header_search = self.navbar_header.find_element_by_class_name('header-tools')
        self.logo = self.navbar_header.find_element_by_class_name('logo')
        self.supernav_options = self.driver.find_element_by_class_name('supernav-verticals')
        for _ in range(10):
            if len(self.driver.find_elements_by_class_name('new-feature')) == 8:
                break
        else:
            raise Exception

    def get_supernav_verticals(self):
        return self.supernav_options.find_elements_by_class_name('supernav-vertical')

    def get_main_content(self):
        return self.driver.find_elements_by_tag_name('main')

    def get_main_content_sections(self):
        return self.get_main_content()[0].find_elements_by_tag_name('section')

    def get_footer_element(self):
        return self.driver.find_elements_by_tag_name('footer')

    def get_sections_from_footer_element(self):
        return self.get_footer_element()[0].find_elements_by_tag_name('section')

    def get_features_section_from_main_content(self):
        return self.get_main_content()[0].find_element_by_class_name('features')

    def get_features_in_features_section(self):
        return self.get_features_section_from_main_content().find_elements_by_class_name('feature')

    def get_links_from_feature(self, feature_element):
        return feature_element.find_elements_by_tag_name('a')

    def get_articles_from_feature(self, feature_element):
        return feature_element.find_elements_by_tag_name('li')
