#!/usr/bin/python3.9
import traceback

import config
import theme

import requests
import time
import random
import vk_api
import threading

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDFillRoundFlatIconButton

from anticaptchaofficial.imagecaptcha import *


class Tab(MDFloatLayout, MDTabsBase):
    pass


class App(MDApp):

    def download_image(self,url, path):
        img_data = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)

    def ls(self):
        solver = imagecaptcha()
        print(1)
        solver.set_verbose(1)
        solver.set_key(config.anti_token)
        print(2)
        vk_session = vk_api.VkApi(token=config.token)
        vk = vk_session.get_api()
        try:
            print(3)
            ss = open('ls.txt', 'r', encoding='utf-8').read().splitlines()
            while 1:
                for s in ss:
                    print(4)
                    try:
                        message = self.root.ids.ls_obr.text + s
                        victim = int(self.root.ids.ls_id.text)
                        r = requests.post(f"https://api.vk.com/method/messages.send?peer_id={victim}&message={message}&access_token={config.token}&v=5.82")
                        answer = r.json()
                        print(answer)
                        if "error" in r.text:
                            if answer["error"]["error_code"] == 14:
                                self.root.ids.ls_lab.text = "Решаем капчу"
                                captcha_sid = answer["error"]["captcha_sid"]
                                captcha_img = answer["error"]["captcha_img"]
                                self.download_image(captcha_img, "captcha.jpeg")
                                captcha_text = solver.solve_and_return_solution("captcha.jpeg")
                                if captcha_text != 0:
                                    self.root.ids.ls_lab.text = f"Текст капчи {captcha_text}"
                                else:
                                    self.root.ids.ls_lab.text = "Задача капчи Ошибка " + str(solver.error_code)
                                self.root.ids.ls_lab.text = "Повторный запрос"
                                r = requests.post(
                                    f"https://api.vk.com/method/messages.send?peer_id={victim}&message={message}&access_token={config.token}&captcha_sid={captcha_sid}&captcha_key={captcha_text}&v=5.81")
                        self.root.ids.ls_lab.text = "Жди..."
                        time.sleep(float(self.root.ids.ls_time.text))
                        self.root.ids.ls_lab.text = "Отправлено"
                    except:
                        self.root.ids.ls_lab.text = traceback.format_exc()
        except:
            self.root.ids.auth_label.text = "Недействительный токен Вконтакте"

    def group(self):
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(config.anti_token)
        vk_session = vk_api.VkApi(token=config.token)
        vk = vk_session.get_api()
        try:
            cs = open('group.txt', 'r', encoding='utf-8').read().splitlines()
            while 1:
                for c in cs:
                    try:
                        message = self.root.ids.group_obr.text + c
                        victim = int(self.root.ids.group_id.text)
                        r = requests.post(f"https://api.vk.com/method/messages.send?peer_id={2000000000+victim}&message={message}&access_token={config.token}&v=5.82")
                        answer = r.json()
                        print(answer)
                        if "error" in r.text:
                            print('captcha')
                            if answer["error"]["error_code"] == 14:
                                self.root.ids.group_lab.text = "Решаем капчу"
                                captcha_sid = answer["error"]["captcha_sid"]
                                captcha_img = answer["error"]["captcha_img"]
                                self.download_image(captcha_img, "captcha.jpeg")
                                captcha_text = solver.solve_and_return_solution("captcha.jpeg")
                                if captcha_text != 0:
                                    self.root.ids.group_lab.text = f"Текст капчи {captcha_text}"
                                else:
                                    self.root.ids.group_lab.text = "Задача капчи Ошибка " + str(solver.error_code)
                                self.root.ids.group_lab.text = "Повторный запрос"
                                r = requests.post(
                                    f"https://api.vk.com/method/messages.send?peer_id={2000000000+victim}&message={message}&access_token={config.token}&captcha_sid={captcha_sid}&captcha_key={captcha_text}&v=5.81")
                        self.root.ids.group_lab.text = "Жди..."
                        time.sleep(float(self.root.ids.group_time.text))
                        self.root.ids.group_lab.text = "Отправлено"
                    except:
                        self.root.ids.group_lab.text = traceback.format_exc()
        except:
            self.root.ids.auth_label.text = "Недействительный токен Вконтакте"

    def start_ls(self):
        threading.Thread(target=self.ls,args=()).start()

    def start_group(self):
        threading.Thread(target=self.group,args=()).start()

    def auth(self):
        vk_token = self.root.ids.vk_token.text
        anti_token = self.root.ids.anti_token.text
        vk_session = vk_api.VkApi(token=vk_token)
        vk = vk_session.get_api()
        try:
            self.root.ids.auth_label.text = f'Вы вошли как\n{vk.account.getProfileInfo()["first_name"]} {vk.account.getProfileInfo()["last_name"]}'
            f = open("config.py", "w",encoding='utf-8')
            f.write(f"# -*- coding: utf-8 -*-\ntoken = '{vk_token}'\nanti_token='{anti_token}'\n")
            f.close()
        except:
            self.root.ids.auth_label.text = "Недействительный токен Вконтакте"

    def change_theme(self,color="Blue"):
        f = open("theme.py","w",encoding="utf-8")
        f.write(f"# -*- coding: utf-8 -*-\ntheme= '{color}'")
        f.close()

    def write_text(self):
        text1=self.root.ids.spam_ls.text
        text2=self.root.ids.spam_group.text
        f = open('ls.txt','w',encoding='utf-8')
        f.write(text1)
        f.close()
        f1 = open('group.txt','w',encoding='utf-8')
        f1.write(text2)
        f1.close()
             
    def build(self):
        #self.theme_cls.colors = colors
        self.theme_cls.primary_palette = theme.theme
        self.theme_cls.accent_palette = "Teal"
        return Builder.load_file("main.kv")

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label,
                      tab_text):
        count_icon = instance_tab.icon
        #print(f'wcm to {count_icon}')
        if self.root.ids.start_button.text == "Записано":
            self.root.ids.start_button.text = "Записать"
        if count_icon == "vk":
            pass
        elif count_icon == "tools":
            pass

    def on_start(self):
        #print(config.token)
        vk_session = vk_api.VkApi(token=config.token)
        vk = vk_session.get_api()
        try:
            self.root.ids.auth_label.text = f'Вы вошли как\n{vk.account.getProfileInfo()["first_name"]} {vk.account.getProfileInfo()["last_name"]}'
        except:
            self.root.ids.auth_label.text = "Вы не вошли в аккаунт"


if __name__ == "__main__":
    App().run()
