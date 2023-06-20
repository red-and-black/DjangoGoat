from behave import when, then

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@when(u'I write a note to "{friend}" with "{content}"')  # noqa: F811
def step_impl(context, friend, content):
    send_button = context.browser.find_element(By.ID, 'send_button')
    receiver_field = context.browser.find_element(By.ID, 'id_receiver')
    content_field = context.browser.find_element(By.ID, 'id_content')

    receiver_field.send_keys(friend)
    content_field.send_keys(content)
    send_button.click()


@when(u'I write a reply to "{friend}" with "{content}"')  # noqa: F811
def step_impl(context, friend, content):
    reply_button = context.browser.find_element(By.ID, 'reply_button')
    content_field = context.browser.find_element(By.ID, 'id_content')

    content_field.send_keys(content)
    reply_button.click()


@when(u"I click 'start a conversation'")  # noqa: F811
def step_impl(context):
    start_convo_button = context.browser.find_element(
        By.PARTIAL_LINK_TEXT,
        'Start',
    )
    start_convo_button.click()


@when(u'I click on the note from "{friend}"')  # noqa: F811
def step_impl(context, friend):
    note_link = context.browser.find_element(By.PARTIAL_LINK_TEXT, friend)
    paragraph = note_link.find_element_by_css_selector('p')
    paragraph.click()


@when(u'I click on the note from "{friend}" on the conversation page')  # noqa: E501,F811
def step_impl(context, friend):
    note_link = context.browser.find_element(By.PARTIAL_LINK_TEXT, friend)
    paragraph = note_link.find_element_by_css_selector('p')
    paragraph.click()


@when(u"I click the back button")  # noqa: F811
def step_impl(context):
    back_button = context.browser.find_element(By.PARTIAL_LINK_TEXT, 'Back')
    back_button.click()


@then("I see the write note form")  # noqa: F811
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.ID, 'send_button')
        )
    )


@then('I see the new note with "{content}"')  # noqa: F811
def step_impl(context, content):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, content)
        )
    )


@then('I see a note from "{friend}"')  # noqa: F811
def step_impl(context, friend):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, friend)
        )
    )


@then("I see the conversation page")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | Conversation'


@then("I see the 404 page")  # noqa: F811
def step_impl(context):
    assert context.browser.title == 'DjangoGoat | 404'


@then("I see the note page")  # noqa: F811
def step_impl(context):
    # assert context.browser.title == 'DjangoGoat | Note Details'
    assert context.browser.title == 'DjangoGoat | Note'


@when("I force browse to note {note_id}")  # noqa: F811
def step_impl(context, note_id):
    note_url = 'https://localhost:8000/note/%s/' % note_id
    context.browser.get(note_url)
