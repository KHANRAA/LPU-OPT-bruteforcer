import requests
from requests_html import HTMLSession
from settings import *
import time

session = requests.Session()
response = session.get(URL)
cookie = session.cookies.get_dict()['JSESSIONID']

time.sleep(5)

session = HTMLSession()
r = session.get(URL)

sel = "FORM > INPUT"
fetched_params = r.html.find(sel, first=False)

params = {}


def calc_content_length():
    global params
    length = 0
    for key in params.keys():
        length += (len(key) + len(params[key]))

    return length + (2 * len(params)) + 6


def get_header():
    global cookie
    header = {
        'HOST': '10.10.0.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://10.10.0.1/24online/webpages/clientlogin.jsp?loginstatus=null&logoutstatus=null&message=null&liverequesttime=null&livemessage=null&url=null&isAccessDenied=null&fromlogout=true&sessionTimeout=null&ipaddress=null&username=null&formsubmiturlIP=null&alerttime=null&deviceType=COMPUTER&ajaxusername=null&autologin=false',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(calc_content_length()),
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


if __name__ == "__main__":
    for each in fetched_params:
        params[each.attrs['name']] = each.attrs['value']

    params['username'] = 'opt10@lpu.com'
    params['password'] = ''

    response = session.post(LOGIN_URL, data=params, headers=get_header())

    select = "FRAMESET > FRAME"
    status = response.html.find(select, first=False)[1].attrs['src']
    status = find_between(status, 'message=', '&').replace('+', ' ').replace('%2F', ' & ')