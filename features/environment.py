from selenium import webdriver


def before_scenario(context, scenario):
    print('Before scenario\n')

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking");
    options.add_experimental_option('w3c', False)
    options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})

    context.driver = webdriver.Chrome(executable_path="/home/luis/Programs/chromedriver", options=options)
    context.driver.implicitly_wait(10)
    context.driver.get("https://www.lovetoknow.com")
    context.before = 'done'


def after_scenario(context, scenario):
    print('After scenario\n')
    context.driver.close()
    context.after = 'done'