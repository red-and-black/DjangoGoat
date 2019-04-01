from behave import given, when, then

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@given("I'm on the dashboard")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/dash/')


@given("I'm on the landing page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/')


@given("I'm on the login page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/login/')


@given("I'm on the profile page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/profile/')


@given("I'm on the profile update page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/profile-update/')


@given("I'm on the sign up page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/sign-up/')


@then(u"I'm logged in")  # noqa: F811
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Log Out')
        )
    )


@then(u"I'm not logged in")  # noqa: F811
@given(u"I'm not logged in")  # noqa: F811
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, 'Sign Up')
        )
    )


@when("I go to the login page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/login/')


@when("I go to the sign up page")  # noqa: F811
def step_impl(context):
    context.browser.get('https://localhost:8000/sign-up/')


@when(u'I enter valid credentials "{username}" and "{password}" and push the login button')  # noqa: E501,F811
def step_impl(context, username, password):
    login_button = context.browser.find_element(By.ID, 'login_button')
    username_field = context.browser.find_element(By.ID, 'id_username')
    password_field = context.browser.find_element(By.ID, 'id_password')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


@when(u'I enter invalid credentials "{username}" and "{password}" and push the login button')  # noqa: E501,F811
def step_impl(context, username, password):
    login_button = context.browser.find_element(By.ID, 'login_button')
    username_field = context.browser.find_element(By.ID, 'id_username')
    password_field = context.browser.find_element(By.ID, 'id_password')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


@when(u'I create "{username}" user with "{password}" password')  # noqa: F811
def step_impl(context, username, password):
    username_field = context.browser.find_element(By.ID, 'id_username')
    password_field = context.browser.find_element(By.ID, 'id_password1')
    password2_field = context.browser.find_element(
        By.ID,
        'id_password2'
    )

    username_field.send_keys(username)
    password_field.send_keys(password)
    password2_field.send_keys(password)

    submit_button = context.browser.find_element(By.ID, 'submit_button')
    submit_button.click()


@when(u'I add a new "{bio}" and click the update button')  # noqa: F811
def step_impl(context, bio):
    bio_field = context.browser.find_element(By.ID, 'id_bio')
    update_button = context.browser.find_element(By.ID, 'update')
    bio_field.send_keys(bio)
    update_button.click()


@when(u'I click the edit profile button')  # noqa: F811
def step_impl(context):
    update_button = context.browser.find_element(
        By.PARTIAL_LINK_TEXT,
        'Edit Profile',
    )
    update_button.click()


@when(u'I click the log out button')  # noqa: F811
def step_impl(context):
    logout_button = context.browser.find_element(
        By.PARTIAL_LINK_TEXT,
        'Log Out',
    )
    logout_button.click()


@then("I see an error message")  # noqa: F811
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.ID, 'error')
        )
    )


@then("I see the profile page")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | Profile'


@then("I see the profile update page")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | Profile Update'


@then("I see the dashboard")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | Dash'


@then("I see the login page")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | Log In'
