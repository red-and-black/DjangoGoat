from behave import fixture, use_fixture

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# From https://behave.readthedocs.io/en/latest/tutorial.html


@fixture
def start_firefox(context):
    # Set up Firefox.
    options = Options()
    # options.headless = True
    context.browser = webdriver.Firefox(
        executable_path='geckodriver',
        options=options,
    )
    yield context.browser

    # Clean up.
    context.browser.quit()


def before_all(context):
    use_fixture(start_firefox, context)
