import platform
import os
import subprocess

from time import sleep

from behave import (
    fixture,
    use_fixture,
)

import django
from django.core.management import call_command

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from zapv2 import ZAPv2


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def start_zap():
    """
    Spawns a new process running ZAP.
    """
    operating_system = platform.system()
    path = 'zaproxy'
    if operating_system == 'Darwin':
        path = '/Applications/OWASP\\ ZAP.app/Contents/Java/zap.sh'

    subprocess.Popen( # nosemgrep
        [path, '-config', 'api.disablekey=true'],
        stdout=open(os.devnull, 'w'),
        stderr=subprocess.STDOUT,
        shell=True
    )

    # If this sleep isn't long enough, there is a race condition and the script
    # hangs.
    sleep(10)


@fixture
def start_firefox(context):
    """
    Starts Firefox in headless mode, and proxying through ZAP.
    """
    options = Options()
    options.headless = True
    zap_proxy = 'localhost:8080'
    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
    # The noProxy list contains domains which Firefox appears to make requests
    # to automatically. If those requests pass through ZAP when scans are
    # running, they interfere with the scans, so set them as not being proxied.
    desired_capabilities['proxy'] = {
        'proxyType': 'MANUAL',
        'ftpProxy': zap_proxy,
        'httpProxy': zap_proxy,
        'sslProxy': zap_proxy,
        'noProxy': [
            'digicert.com',
            'firefox.com',
            'mozilla.com',
            'mozilla.net',
        ],
    }
    context.browser = webdriver.Firefox(
        executable_path='geckodriver',
        options=options,
        capabilities=desired_capabilities,
    )
    yield context.browser

    # Clean up once the tests finish.
    context.browser.quit()


def recreate_database():
    """
    Destroys and the recreates the SQLite database so each test run starts with
    a clean slate.
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangogoat.settings'
    django.setup()
    database_path = os.path.join(BASE_DIR, 'db.sqlite3')
    if os.path.exists(database_path):
        os.remove(database_path)
    call_command('migrate', '--noinput')


def before_all(context):
    """
    This function is run before the BDD tests are run.
    """
    recreate_database()
    start_zap()
    use_fixture(start_firefox, context)


def after_all(context):
    """
    This function is run after the BDD tests are run. We use it to kick off the
    ZAP scanning.
    """
    # General preparation.
    zap = ZAPv2(apikey=None)
    base_url = 'https://localhost:8000'
    logged_out_indicator_regex = r'\QSign Up\E'
    logout_url_regex = '%s/logout.*' % base_url
    main_context_regex = '%s.*' % base_url
    static_url_regex = '%s/static.*' % base_url
    zap_context_id = 1
    zap_context_name = 'Default Context'

    # Set ZAP's context. This means the range of URLs which ZAP will scan.
    # Note that Behave's context, as passed into this function, it a totally
    # different concept to ZAP's context.
    print(
        main_context_regex + ' -> ' +
        zap.context.include_in_context(
            contextname=zap_context_name,
            regex=main_context_regex
        )
    )

    # General script preparation.
    script = zap.script
    features_dir = os.path.join(BASE_DIR, 'features')
    script_engine = 'Oracle Nashorn'

    # Set up a custom ZAP Http Sender script which improves ZAP's handling of
    # Django CSRF tokens.
    http_sender_script_name = 'CSRFInterceptor.js'
    http_sender_script_path = os.path.join(
        features_dir,
        http_sender_script_name
    )
    print(
        'Load HTTP Sender script: ' + http_sender_script_name + ' -> ' +
        script.load(
            scriptname=http_sender_script_name,
            scripttype='httpsender',
            scriptengine=script_engine,
            filename=http_sender_script_path,
        )
    )
    print(
        'Enable HTTP Sender script: ' + http_sender_script_name + ' -> ' +
        script.enable(scriptname=http_sender_script_name)
    )

    # Set up Django-specific ZAP Authentication script.
    auth_method = 'scriptBasedAuthentication'
    auth_script_name = 'DjangoAuthentication.js'
    auth_script_path = os.path.join(features_dir, auth_script_name)
    print(
        'Load Authentication script: ' + auth_script_name + ' -> ' +
        script.load(
            scriptname=auth_script_name,
            scripttype='authentication',
            scriptengine=script_engine,
            filename=auth_script_path,
        )
    )

    # Set the authentication method.
    auth = zap.authentication
    authParams = (
        'scriptName=' + auth_script_name + '&'
        'Username field=username&'
        'Password field=password&'
        'Target URL=%s/login/' % base_url,
    )
    print(
        'Set authentication method: ' + auth_method + ' -> ' +
        auth.set_authentication_method(
            contextid=zap_context_id,
            authmethodname=auth_method,
            authmethodconfigparams=authParams
        )
    )

    # Set the logged-out indicator.
    print(
        'Define LoggedOut indicator: ' + logged_out_indicator_regex +
        ' -> ' +
        auth.set_logged_out_indicator(
            contextid=zap_context_id,
            loggedoutindicatorregex=logged_out_indicator_regex
        )
    )

    # Define the users
    # Note that the ZAP scans are run once for each user, so defining 3 users
    # means ZAP will scan your app three times. Only define more than one user
    # here if you have different types of users which you'd like ZAP to scan
    # for.
    users = zap.users
    user_list = [
        {
            'name': 'ImBaaaaad',
            'credentials': 'Username=ImBaaaaad&Password=Appletr33!'
        }
    ]
    user_ids = []
    for user in user_list:
        username = user.get('name')
        print('Creating user ' + username)
        user_id = users.new_user(contextid=zap_context_id, name=username)
        user_ids.append(user_id)
        print(
            'User ID: ' + user_id + '; username -> ' +
            users.set_user_name(
                contextid=zap_context_id, userid=user_id, name=username
            ) +
            '; credentials -> ' +
            users.set_authentication_credentials(
                contextid=zap_context_id,
                userid=user_id,
                authcredentialsconfigparams=user.get('credentials')
            ) +
            '; enabled -> ' +
            users.set_user_enabled(
                contextid=zap_context_id, userid=user_id, enabled=True
            )
        )

    # Set up the spider.
    # The logout url is excluded so that ZAP can't log itself out by mistake.
    # The static files are excluded because they slow the scan down for no real
    # benefit.
    spider = zap.spider
    spider.exclude_from_scan(logout_url_regex)
    spider.exclude_from_scan(static_url_regex)

    # Spider the app as an unauthenticated user.
    print('Spidering %s as an unauthenticated user.' % base_url)
    scan_id = spider.scan(base_url)
    while (int(spider.status(scan_id)) < 100):
        print('Spider progress: %s%%' % spider.status(scan_id))
        sleep(5)
    print('***RESULTS***')
    for result in sorted(spider.results()):
        print(result)
    print('')

    # # Give the passive scanner a chance to finish
    while (int(zap.pscan.records_to_scan) > 0):
        sleep(1)

    # Set up the active scanner.
    # The logout url is excluded so that ZAP can't log itself out by mistake.
    # The static files are excluded because they slow the scan down for no real
    # benefit.
    ascan = zap.ascan
    ascan.exclude_from_scan(logout_url_regex)
    ascan.exclude_from_scan(static_url_regex)

    # Scan the app one user at a time.
    for user_id in user_ids:
        print('Starting scans as user %s.' % user_id)

        # Run the spider.
        scan_id = spider.scan_as_user(
            contextid=zap_context_id,
            userid=user_id,
            url=base_url,
            maxchildren=None,
            recurse=True,
            subtreeonly=None
        )
        print('Spidering (scan id %s).' % scan_id)
        sleep(5)
        while (int(spider.status(scan_id)) < 100):
            print('Progress: %s%%' % spider.status(scan_id))
            sleep(2)
        print('***RESULTS***')
        for result in sorted(zap.spider.results()):
            print(result)
        print('')

        # # Give the passive scanner a chance to finish
        while (int(zap.pscan.records_to_scan) > 0):
            sleep(1)

        # Run the active scan.
        scan_id = ascan.scan_as_user(
            url=base_url,
            contextid=zap_context_id,
            userid=user_id,
            recurse=True,
            scanpolicyname=None,
            method=None,
            postdata=True
        )
        print('Active scanning (scan id %s).' % scan_id)
        while (int(ascan.status(scan_id)) < 100):
            print('Progress: %s%%' % ascan.status(scan_id))
            sleep(5)

    print('All scans completed')

    # Report the results
    print('Zap hosts: ' + ', '.join(zap.core.hosts))
    alerts = zap.core.alerts()
    if alerts:
        print('There are %s Zap alerts.' % len(alerts))
        with open('report.html', 'w') as f:
            f.write(zap.core.htmlreport())
        print('A report has been saved.')
    else:
        print('There are no Zap alerts.')
