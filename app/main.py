import os
from time import sleep

import threading

import webview
import keyboard


from calculator import Calculator
from server import start_server
from user import User
from settings import *



def on_resized(width, height):
    print('pywebview window is resized. new dimensions are {width} x {height}'.format(width=width, height=height))


def pass_test():
    window.load_url("https://www.ratatype.ua/typing-test/test/en/")
    sleep(2)
    keyboard.send("ENTER")
    sleep(1)
    while window.get_elements('span.wgreen'):
        try:
            letter = window.get_elements('span.wgreen')[0]['innerHTML']
            if letter == "" or \
                    letter == " " or \
                    letter is None:
                keyboard.write(" ")
            else:
                keyboard.write(letter)
                sleep(0.1)
        except Exception as e:
            print(str(e))


def save_results(content, user):
    speed = content[0]["innerText"]
    accuracy = content[1]["innerText"]
    lang = window.get_elements("img.img-responsive")[0]['src'].split('/')[-2]
    print(f"{speed=}\n{accuracy=}\n{lang=}\n{user=}")
    if speed.isnumeric():
        calc = Calculator(speed=speed,
                          accuracy=accuracy,
                          lang=lang,
                          user=user)
        calc.save_data()
        print('result is saved!')
        window.evaluate_js("alert('result is saved!')")
        # window.load_url(START_PAGE)
        window.evaluate_js("""
        var tag = document.createElement("a");
        var text = document.createTextNode("Перейти на стартовую страницу Ratatype Simulator!");
        tag.appendChild(text);
        tag.href = "http://0.0.0.0:80/start";
        var element = document.getElementsByClassName("col-xs-12 col-sm-5")[0];
        tag.classList.add('btn');
        tag.classList.add('btn-light');
        tag.classList.add('w-100');
        tag.classList.add('add-top');
        element.appendChild(tag);
        """)


def on_loaded():
    global user
    url = window.get_current_url()
    url_arr = url.split("/")

    print(url)

    if "mytest" in url_arr:
        pass_test()
        user.set_user("robot")

    if "start" in url_arr:
        window.load_url(START_PAGE)
        user = User()

    if "complete" in url_arr:
        content = window.get_elements('span.fs-36')
        save_results(content, user.get_user())


if __name__ == "__main__":
    user = User()
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    window = webview.create_window('Ratatype Simulator', START_PAGE,
                                   confirm_close=True,
                                   width=1023, height=600)
    window.events.loaded += on_loaded
    webview.start()