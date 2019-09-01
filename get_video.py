#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
from sys import platform
from bs4 import BeautifulSoup


def get_html(link):
    """Return html page from url."""
    fp = urllib.request.urlopen(link)
    bytes = fp.read()
    page = bytes.decode("utf8")
    fp.close()
    return page


if __name__ == '__main__':
    course_link = input('Введите ссылку на курс: ')
    path = input('Введите путь: ')
    path = '/media/amerohful/Диск H1/courses/' + path
    if not os.path.isdir(path):
        os.mkdir(path)
    if not path == '' and not path == '/' or not path == '\\':
        path += '\\' if platform == 'win32' else '/'

    print('Download course page...')
    course = BeautifulSoup(get_html(course_link), 'html.parser')
    print('Course page was downloaded sucsessful!\nFind video page...')

    video_course = course.find('div', {
        'class': 'videoteka_courseList videotekaCenterBlock videoteka_items'
    })
    videos = [a.get('href') for a in video_course.findAll('a', href=True)]
    print('Video page was found sucsessful!\nFind links...')

    videos_link = []
    for link in videos:
        page_link = BeautifulSoup(
            get_html('https://www.jv.ru{}'.format(link)), 'html.parser')
        videos_link.append((len(videos_link) + 1, page_link.find('link', {
            'class': 'hideItem', 'itemprop': 'url'}).get('href')))
    print('Links was found sucsessful!')

    for link in videos_link:
        print('Download video number {}'.format(link[0]))
        try:
            print('Download start...')
            urllib.request.urlretrieve(
                link[1], filename='{}{}.mp4'.format(path, link[0]))
            print('Video number {} was downloaded!'.format(link[0]))
        except Exception as e:
            print(e)
