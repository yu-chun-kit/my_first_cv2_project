#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: get_travel.py
Programmer: Johnson
Email: johnson37siumen@hotmail.com
Github: https://github.com/yu-chun-kit/
Date : 2019-02-09
Description: useless program
"""
import os
# import re
import random
import time

import cv2
import requests
from requests_html import HTMLSession

from getsizes import getsizes

session = HTMLSession()


def get_list(src_url, folder):
    """ search pic from web"""
    time.sleep(3.1415926)
    response = session.get(src_url)  # return a session obj
    content = response.html.find('div.first-child', first=True)
    div_list = content.find('div.post')
    # print("1st size:", len(div_list))
    pictures = []
    urls = []
    descriptions = []
    # isdestroyed, height, width
    details = []
    # for div in div_list:
    for div in div_list:
        url = div.find('a.image-list-link', first=True).attrs['href']
        pic = url.split('/')[-1]
        url = "https://i.imgur.com/" + url.split('/')[-1] + ".jpg"
        desc = div.find('div.hover ', first=True).find('p', first=True).text
        print(url)
        print(desc)
        time.sleep(random.random() * 2 + 1)
        pictures.append(pic)
        descriptions.append(desc)
        urls.append(url)
        detl = save_image(url, folder)
        details.append(detl)

    # filename = "./image/japan/" + src_url.split("/")[-1] + ".json"
    filename = "./image/" + folder + "/" + src_url.split("/")[-1] + ".html"
    print('filenmae = ' + filename)
    with open('prefix.txt', 'r') as preFile, open('postfix.txt', 'r') as postFile, open(filename, "a+") as f_obj:
        idNo = 0
        # lines = preFile.readlines()
        # lines = [l for l in lines if "ROW" in l]
        # f_obj.writelines(lines)
        f_obj.write('    <div class="img-container">\n')
        for i, pic in enumerate(pictures):
            link = src_url + "/" + pic

            if not details[i][0]:
                # f_obj.write('      <div class=\"drp\" data-img-id=\"' +
                            # str(idNo) + '\">\n')
                # idNo += 1
                # f_obj.write(
                # '          <!--<img src=\"image/' + folder + '/' + pic +
                # '.jpg\" alt=\"\" width=\"200\" height=\"200\">-->\n')
                f_obj.write('          <img src=\"' + urls[i] +
                            '\" alt=\"\" width=\"300\" height=\"220\">\n')
                # f_obj.write("          <div class=\"drpCon\">\n")
                # f_obj.write('              <!--<img src=\"image/' + folder +
                # '/' + pic + '.jpg\" height=\"' +
                # str(details[i][1]) + '\" width=\"' +
                # str(details[i][2]) + '\" alt=\"\">-->\n')
                # f_obj.write('              <img src=\"' + urls[i] +
                            # '\" height=\"' + str(details[i][1]) +
                            # '\" width=\"' + str(details[i][2]) +
                            # '\" alt=\"\">\n')
                # f_obj.write('              <a href=\"' + link +
                            # '\" class=\"desc\" target=\"videoframe\"' + '>' +
                            # descriptions[i] + '</a>\n')
                # f_obj.write('          </div>\n')
                # f_obj.write('      </div>\n')
        f_obj.write('    </div>\n')
        # lines = []
        # lines = postFile.readlines()
        # f_obj.writelines(lines)


# 保持大图
def save_image(img_url, folder):
    """Save some image"""
    destroyed = False
    abbr = img_url.split("/")[-1]
    try:
        size, width, height = getsizes(img_url)
        print(height, width, end=", dispaly size = ")
        if (height == 81 and width == 161):
            print("image --> " + abbr + " may no longer exist")
            destroyed = True
        if (height == 0 and width == 0):
            print("image --> " + abbr + "can not get the size")
            destroyed = True
        if (height > 2500 or width > 2500):
            print("image --> " + abbr + " height or width too large")
            destroyed = True
        if (height / width > 2.5 or width / height > 2.5):
            print("image --> " + abbr + " has unusual ratio")
            destroyed = True
        elif size > 1737905:
            print("image --> " + abbr + " size is too large")
            destroyed = True
        else:
            if width > 320:
                div_num = width // 320
                height = height // div_num
                width = width // div_num
                print(height, width)
    except AttributeError:
        print("Has error (may be gif)!!!!")
        destroyed = True
    if destroyed:
        print("picture not suitable")
        print("-------------------")
        return [destroyed, 0, 0]
    print("-------------------")
    return [destroyed, height, width]
    # img_response = requests.get(img_url)
    # t = int(round(time.time() * 1000))
    # f = open('./image/japan/{0}'.format(abbr[-1]), 'ab')
    # f = open('./image/' + folder + '/{0}'.format(abbr), 'ab')
    # f.write(img_response.content)
    # f.close()


def main():
    """ main function of get_travel """
    # site = "https://imgur.com/r/japanpics"
    site = "https://imgur.com/r/SouthKoreaPics"
    folder = "koera2"
    directory = os.getcwd() + "/image/" + folder
    if site.endswith('/'):
        site = site[:-1]
    if not os.path.exists(directory):
        print("create folder at " + directory)
        os.makedirs(directory)
    else:
        print("folder exists")

    # "https://imgur.com/r/ChinaPics"
    # "https://imgur.com/r/japanpics"
    print("The site is ", site)
    get_list(site, folder)
    print("fin")


if __name__ == '__main__':
    main()
