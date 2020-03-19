from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }


def before_scenario(context, scenario):
    print('Before scenario\n')

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking");
    options.add_experimental_option('w3c', False)
    options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})
    options.add_argument("--user-data-dir=/home/luis/Programs/google-chrome-profile-data/google-chrome")

    context.driver = webdriver.Chrome(executable_path="/home/luis/Programs/chromedriver", options=options,
                                      service_args=["--error", "--log-path=/var/tmp/selenium.log"],
                                      desired_capabilities=d)
    context.driver.implicitly_wait(10)
    context.driver.get("https://www.lovetoknow.com")
    context.before = 'done'
    context.driver_wait = WebDriverWait(context.driver, 20, ignored_exceptions=(StaleElementReferenceException, ))

def after_scenario(context, scenario):
    print('After scenario\n')
    context.driver.close()
    context.after = 'done'