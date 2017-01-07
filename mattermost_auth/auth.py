import click
import os
import requests
import sys

from cefpython3 import cefpython as cef

FILE = os.path.join(os.path.expanduser('~'), '.mmauthtoken')


class CookieVisitor(object):

    def __init__(self, browser):
        self.browser = browser
        self.token = None

    def Visit(self, cookie, count, total, delete):
        if cookie.GetName() == 'MMAUTHTOKEN':
            self.token = cookie.GetValue()
            self.browser.CloseBrowser()

            return False
        return True


class Handler(object):

    def GetCookieManager(self, browser, url):
        if not browser.GetUserData("cookieManager"):
            browser.SetUserData("cookieManager", cef.CookieManager.CreateManager(
                os.path.join(os.path.expanduser('~'), '.mmauthcookies')))
        return browser.GetUserData("cookieManager")


def read_token(domain):
    try:
        with open(FILE) as f:
            token = f.read().strip()
            resp = requests.get('https://%s/api/v3/users/me' % domain, headers={
                'Authorization': 'Bearer %s' % token,
            })
            resp.raise_for_status()
            return token
    except Exception:
        return None


def write_token(token):
    with os.fdopen(os.open(FILE, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as f:
        f.write(token)


def get_token_from_browser(domain):
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    browser = cef.CreateBrowserSync(url="https://%s/login/sso/saml" % domain)
    browser.SetClientHandler(Handler())

    import threading
    import time

    v = CookieVisitor(browser)

    def cookies():
        while v.token is None:
            if browser.GetUserData('cookieManager'):
                browser.GetUserData("cookieManager").VisitAllCookies(v)
            time.sleep(1)

        cef.PostTask(0, lambda: cef.QuitMessageLoop())

    t = threading.Thread(target=cookies)
    t.start()
    cef.MessageLoop()

    if not v.token:
        sys.exit(1)

    resp = requests.post('https://%s/api/v3/users/attach_device' % domain, json={
        'device_id': 'android:mmtokenclient'
    }, headers={'Authorization': 'Bearer %s' % v.token})
    resp.raise_for_status()
    write_token(v.token)
    return v.token


@click.command()
@click.option('-d', '--domain', required=True, help='Domain to use')
@click.option('-t', '--team', required=True, help='Mattermost team name')
@click.option('-u', '--user', required=True, help='Username')
def main(domain, team, user):
    token = read_token(domain)
    if not token:
        token = get_token_from_browser(domain)

    print 'login %s %s %s MMAUTHTOKEN=%s' % (domain, team, user, token)


if __name__ == '__main__':
    main()
