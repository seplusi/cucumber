from behave import then
from random import randrange
import requests
from features.page_objects.main_page import MainPage
from features.page_objects.feature_page import FeaturePage
import selenium
import time
from selenium.webdriver.common.action_chains import ActionChains

supernav_verticals_text = ['BEAUTY & FASHION', 'ENTERTAINMENT', 'HEALTH', 'HOME & GARDEN', 'TECHNOLOGY', 'MONEY', 'LIFESTYLE', 'TRAVEL & VACATIONS']

@then(u'I can validate lovetoknow opens and shows page details')
def steps_impl(context):
    main_page = MainPage(context.driver)
    list_items = main_page.get_supernav_verticals()

    assert [item.text for item in list_items] == supernav_verticals_text, f'{get_page_sections}'
    for item in list_items:
        assert item.is_displayed()

    assert len(main_page.get_main_content()) == 1

    page_sections = main_page.get_main_content_sections()
    assert len(page_sections) == 2
    assert [section.is_displayed() for section in page_sections] == [True, True]

    footer = main_page.get_footer_element()
    assert len(footer) == 1

    sections = main_page.get_sections_from_footer_element()
    assert len(sections) == 2
    assert [section.is_displayed() for section in sections] == [True, True]

@then(u'I can validate New & Popular section is displayed')
def steps_impl(context):
    main_page = MainPage(context.driver)

    features_section = main_page.get_features_section_from_main_content()
    assert 'New & Popular Topics' in features_section.text.split('\n')
    assert features_section.is_displayed()

@then(u'I can validate all links in section work')
def steps_impl(context):
    main_page = MainPage(context.driver)
    features_in_features_section = main_page.get_features_in_features_section()
    for feature in features_in_features_section:
        links = feature.find_elements_by_tag_name('a')
        assert len(links) == 4
        for link in links:
            assert link.is_displayed()
            assert (requests.head(link.get_attribute('href')).status_code == 200)

            print('%s : OK' % (link.get_attribute('href')))

@then(u'I can write comment in any article')
def steps_impl(context):
    main_page = MainPage(context.driver)

    main_page.driver.find_element_by_css_selector('a.gdpr-button.dismiss-button').click()

    features = main_page.get_features_in_features_section()
    random_number = randrange(len(features))
    feature_name = features[random_number].text.split('\n')[0]

    articles = main_page.get_articles_from_feature(features[random_number])
    random_number2 = randrange(len(articles))

    action = ActionChains(context.driver)
    action.move_to_element(articles[random_number2]).perform()

#    print(articles[random_number2].location_once_scrolled_into_view)
    article_name = articles[random_number2].text

    print('%s' % article_name)
    print('  %d' % (random_number2))

    for _ in range(10):
        try:
            print(articles[random_number2].click())
            break
        except selenium.common.exceptions.ElementClickInterceptedException as err:
            time.sleep(0.1)
            print('Waited a bit')
    else:
        raise Exception

    feature_page = FeaturePage(context.driver, feature_name)
    first_comment_box = feature_page.get_all_comment_boxes()[0]
    feature_page.click_comment_box(first_comment_box)

    feature_page.driver.find_element_by_class_name('placeholder')
    print('gfd')




