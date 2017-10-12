#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
import re

RAKUTENSEC_SITE = 'http://m.rakuten-sec.co.jp'

def get_login_page():
    r = requests.get(RAKUTENSEC_SITE)
    r.encoding = 'cp932'
    soup = BeautifulSoup(r.text, 'html.parser')
    btn = soup.find(accesskey='1')
    return btn.get('href')

def login(id, password):
    login_url = get_login_page()
    login_page = requests.get(RAKUTENSEC_SITE + login_url)
    login_page.encoding = 'cp932'
    login_form = BeautifulSoup(login_page.text, 'html.parser')
    form = login_form.find('form')
    params = {}
    for input in form.find_all('input'):
        input_name = input.get('name')
        input_type = input.get('type')
        if input_type == 'submit':
            pass
        elif input_name == 'loginPassword':
            params[input_name] = password
        elif input_name == 'loginId':
            params[input_name] = id
        else:
            params[input_name] = input['value']
    res = requests.post(form.attrs['action'], data=params)
    res.encoding = 'cp932'
    return (res.url, BeautifulSoup(res.text, 'html.parser'))

def logout(ctx):
    url = ctx[0]
    logout_link = ctx[1].find(accesskey=9)['href']
    
    logout_url = urljoin(url, logout_link)
    res = requests.get(logout_url)
    res.encoding = 'cp932'
    return BeautifulSoup(res.text, 'html.parser')

def get_page(ctx, link_str):
    url = ctx[0]
    links = ctx[1].find_all('a')
    for link in links:
        if link.string == link_str:
            break
    else:
        return None
    res = requests.get(urljoin(url, link['href']))
    res.encoding = 'cp932'
    return (res.url, BeautifulSoup(res.text, 'html.parser'))

def search_stock(ctx, code):
    (url, page) = (ctx[0], ctx[1])
    search_form = page.find('form')
    params = {'security': code}
    res = requests.post(urljoin(url, search_form['action']), data=params)
    res.encoding = 'cp932'
    return (res.url, BeautifulSoup(res.text, 'html.parser'))

def get_option(select_box):
    selection = select_box.find('option', selected='selected')
    if selection is None:
        selection = select_box.find('option')
    return selection['value']

def get_hidden_params(form):
    params = {}
    hidden_input = form.find_all('input', type='hidden')
    for i in hidden_input:
        params[i['name']] = i['value']
    return params

def make_order(ctx, pin, num_stocks):
    (url, page) = (ctx[0], ctx[1])
    form = page.find('form', name='mt1DetailForm')
    params = get_hidden_params(form)
    params['qty'] = '%d' % num_stocks
    params['limitPriceCondition'] = 'nariyuki' # 'sashine'
    # params['limitPrice']
    params['executionCondition'] = '1' # today
    params['orderTerm'] = get_option(form.find('select', name='orderTerm'))
    params['specifiedAccountKbn'] = 'tokutei'
    params['setOrderKbn'] = get_option(form.find('select', name='setOrderKbn'))
    params['dealingsPw'] = pin
    params['omission'] = 'noConfirmation' # or confirmation
    res = requests.post(urljoin(url, form['action']), data=params)
    res.encoding = 'cp932'
    return (res.url, BeautifulSoup(res.text, 'html.parser'))

id = sys.argv[1]
password = sys.argv[2]
pin = sys.argv[3]
ctx = login(id, password)
ctx = get_page(ctx, u'株式取引')
ctx = get_page(ctx, u'現物買い注文')
#ctx = search_stock(ctx, '6758')
ctx = search_stock(ctx, '4406')
txt = ctx[1]
m = re.match(r'^\(単元株数(\d+)株\)', txt.text)
if m is not None:
    print('単元株', m.group(1))
#make_order(ctx, pin, 100)

print(ctx[0], ctx[1])

print(logout(ctx))

