from behave import then
import string
import random
import requests
from features.page_objects.main_page import MainPage
from features.page_objects.feature_page import FeaturePage
import selenium
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

supernav_verticals_text = ['BEAUTY & FASHION', 'ENTERTAINMENT', 'HEALTH', 'HOME & GARDEN', 'TECHNOLOGY', 'MONEY', 'LIFESTYLE', 'TRAVEL & VACATIONS']

@then(u'I can validate lovetoknow opens and shows page details')
def steps_impl(context):
    main_page = MainPage(context.driver, context.driver_wait)

    list_items = main_page.get_supernav_verticals()

    assert [item.text for item in list_items] == supernav_verticals_text, f'{[item.text for item in list_items]}'
    assert len(main_page.get_main_content()) == 1
    assert len(main_page.get_main_content_sections()) == 2
    assert len(main_page.get_footer_element())
    assert len(main_page.get_sections_from_footer_element())

@then(u'I can validate New & Popular section is displayed')
def steps_impl(context):
    main_page = MainPage(context.driver, context.driver_wait)

    features_section = main_page.get_features_section_from_main_content()
    assert 'New & Popular Topics' in features_section.text.split('\n')

@then(u'I can validate all links in section work')
def steps_impl(context):
    main_page = MainPage(context.driver, context.driver_wait)
    features_in_features_section = main_page.get_features_in_features_section()
    for feature in features_in_features_section:
        links = feature.find_elements_by_tag_name('a')
        assert len(links) == 4
        for link in links:
            assert link.is_displayed()
            assert (requests.head(link.get_attribute('href')).status_code == 200)

            print('%s : OK' % (link.get_attribute('href')))

@then(u'I can open any article and a new page is shown')
def steps_impl(context):
    main_page = MainPage(context.driver, context.driver_wait)

    article_name, feature_name = main_page.click_random_article()

    feature_page = FeaturePage(context.driver, context.driver_wait, feature_name, article_name)
    assert feature_page.verify_headers() == (feature_name, article_name)

@then(u'I can write comment in any article')
def steps_impl(context):
    main_page = MainPage(context.driver, context.driver_wait)

    article_name, feature_name = main_page.click_random_article()

    feature_page = FeaturePage(context.driver, context.driver_wait, feature_name, article_name)
    assert feature_page.verify_headers() == (feature_name, article_name)

    # Click first comment box
    feature_page.click_first_comment_box()

    # Make the block where comments are visible. It's "display: block"
    context.driver.execute_script('document.getElementById("disqus_thread").style.display=\'inline\';')

    # Switching to the iframe (#document) and then using the normal query
    iframe = context.driver.find_elements_by_css_selector('div#disqus_thread > iframe')[0]

    # Because elements I need are under #documents
    context.driver.switch_to_frame(iframe)

    # Click login and use disqus login account. It's not necessaryh to type user/passwd because google chrome stores that info. It logs in automatically
    feature_page.login_using_disqus()
    assert context.driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.username'))).text == 'Luis Arcanjo'

    # Write the comment
    comment = feature_page.write_comment()

    # Verify comment
    post_comments_list = context.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.post-message > div > p')))
    users_list = context.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.author.publisher-anchor-color > a')))
    assert len(post_comments_list) == len(users_list)
    for index in range(len(post_comments_list)):
        if context.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.post-message > div > p')))[index].text == comment:
            assert context.driver_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.author.publisher-anchor-color > a')))[index].text == 'Luis Arcanjo'
            break
    else:
        assert False
