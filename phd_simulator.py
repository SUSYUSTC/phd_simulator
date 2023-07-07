import time
import numpy as np
from splinter import Browser
browser = Browser('chrome')
browser.visit("https://research.wmz.ninja/projects/phd/index.html")
time.sleep(1)
preference_order = [
    'offer',
    'break',
    'fix',
    'resubmit',
    'draft paper',
    'Conduct experiments',
    'major result',
    'preliminary result',
    'developing an idea',
    'Read',
]


def get_hope():
    text = browser.find_by_id('hope_meter')[0].text
    return int(text.split(' ')[1].split('/')[0])


def get_time():
    text = browser.find_by_id('time_meter')[0].text
    return int(text.split(' ')[1]), int(text.split(' ')[3])


def get_all():
    buttons = browser.find_by_css('.btn')
    texts = [item.text for item in buttons]
    return texts


def print_info():
    global success, tot
    print()
    print('totol times', tot)
    print('number success', len(success))
    print(success)
    if len(success) > 0:
        print('mean success time in month:', np.mean(success))
    print()


def find_specific_choice(choice):
    buttons = browser.find_by_css('.btn')
    texts = [item.text for item in buttons]
    texts = [item for item in texts if item != '']
    for text in texts:
        if choice in text:
            return True
    return False


def make_specific_choice(choice):
    buttons = browser.find_by_css('.btn')
    texts = [item.text for item in buttons]
    texts = [item for item in texts if item != '']
    for button, text in zip(buttons, texts):
        if choice in text:
            button.click()
            return text


def make_choice_by_order(preference_order):
    buttons = browser.find_by_css('.btn')
    texts = [item.text for item in buttons]
    texts = [item for item in texts if item != '']
    for choice in preference_order:
        match = [choice in text for text in texts]
        if True in match:
            index = match.index(True)
            buttons[index].click()
            return texts[index]
    return


def skip_unuseful():
    buttons = browser.find_by_css('.btn')
    texts = [item.text for item in buttons]
    texts = [item for item in texts if item != '']
    if len(texts) == 1:
        buttons[0].click()
        return texts[0]


def make_choice():
    year, month = get_time()
    result = skip_unuseful()
    if result is not None:
        return result

    #hope = get_hope()
    #if hope < 30:
    #    if make_specific_choice('Slack'):
    #        return 'Slack'
    if year == 1 and month >= 8:
        if find_specific_choice('Prepare'):
            return make_specific_choice('Prepare')
    return make_choice_by_order(preference_order)


success = []
tot = 0
verbose = True
while True:
    try:
        year, month = get_time()
        tot_month = year * 12 + month
        text = make_choice()
        time.sleep(1)
        if text is None:
            if verbose:
                print('sleep')
            time.sleep(1)
            continue
        if verbose:
            print(text)
        if 'start again' in text:
            print('finished')
            tot += 1
            print_info()
        elif 'thesis' in text:
            success.append(tot_month)
    except BaseException as e:
        print('get error')
        print(e.__repr__())
        time.sleep(1)
