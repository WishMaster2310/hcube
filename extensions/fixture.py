# coding: utf-8

import json
import os


"""
Расширение, которое реализует подгрузку контента из json

Использование:

a) Использование сквозных фикстур:
    Фикстуры, которые должны присутствовать на всех страницах
    определяются в файле fixture/__base.json

б) Фикстуры для определенных страниц:
    В директроии fixture/ создаем файл, одноименный с названием
    страницы, на которую фикстура должна подгружаться 
    (для файла templates/foo_bar.html создаем фикстуру fixture/foo_bar.json)

Использование в шаблоне:
    Фикстуры автоматически подгружаются в контекст, далее в шаблоне используются 
    привычными способами. ({{ variable }})

"""
FIXTURE = 'fixture'

def load_fixture(directory=None, page=None, path=None):
    base_fixture = 'fixture/__base.json'
    if directory or page:
        page_fixture = '%s.json' % os.path.join(FIXTURE, directory, page)
    elif path:
        page_fixture = '%s.json' % path
    else:
        return ''
    fixture_ctx = {
        'base': load(base_fixture),
        'page': load(page_fixture),
    }
    return fixture_ctx


def load(fixture_name):
    try:
        fixture = open(fixture_name)
    except IOError:
        return {}
    else:
        try:
            data = json.load(fixture)
        except ValueError:
            print u'Error load %s' % fixture_name
            return {}
        else:       
            return data 