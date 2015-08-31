#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import os
import re

from flask import Flask
from flask import render_template
from flask import make_response
from functools import update_wrapper
from jinja2.exceptions import TemplateNotFound

from extensions.fixture import load_fixture, FIXTURE


app = Flask(__name__)
#app.jinja_env.add_extension('jinja2htmlcompress.SelectiveHTMLCompress')

PATH = os.path.dirname(__file__)
TEMPLATE_DIR = 'templates'
STATIC_DIR = 'static'
EXPORT_DIR = 'export'

# extensions
TEMPLATE_LIST = 'template_list'
ENABLE_EXTINSIONS = (
    FIXTURE,
    TEMPLATE_LIST,
)

def nocache(f):
    """
    Отменяем кеш
    """

    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

class Node():
    """
    Класс элемента списка файлов и директорий. Маленький простенький "нодик".
    """

    isdir = False
    name = ''
    path = ''
    files = []

    def __init__(self, isdir = True, name = '', path = '', files = []):
        self.isdir = isdir
        self.name = name
        self.path = path.replace( os.path.join(PATH, TEMPLATE_DIR) , '')\
                        .replace('.html', '')\
                        .replace('\\', '/')

        self.files = files

def __get_files(directory):
    """
    Хелпер для рекурсивного пробега по директории с темплейтами. На случай,
    если у нас появляются уровни вложенности
    """

    files = []
    for f in os.listdir(directory):
        # Если это директория или html файлик, то работаем дальше
        if (os.path.isdir( os.path.join(directory, f))
                or '.html' in f) \
            and not f.startswith('__'):

            # Если это папочка, то вот она - рекурсия!
            if os.path.isdir(os.path.join(directory,f)):
                files.append( Node(True, f,
                                    os.path.join(directory, f),
                                    __get_files( os.path.join(directory,f))) )
                continue

            files.append( Node(False, f, os.path.join(directory, f)) )

    return files


@nocache
@app.route('/')
@app.route('/<page>/')
@app.route('/<directory>/<page>/')
def any_page(directory='/', page='/'):
    """
    Собственно, роут для шаблонов. Открывает наши файлики
    """
    node = Node(True, TEMPLATE_DIR, '/',
                __get_files( os.path.join(PATH, TEMPLATE_DIR)))

    ctx = {}
    # extends
    if FIXTURE in ENABLE_EXTINSIONS:
        fixture = load_fixture(directory=directory, page=page)
        ctx.update(fixture)

    if page == '/':
        return render_template('__list.html',
            node=node, **ctx)
    try:
        template_name = os.path.join(directory, page + '.html').replace('\\', '/')
        # templates list
        if TEMPLATE_LIST in ENABLE_EXTINSIONS:
            ctx['templates'] = render_template('__files_list.html', node=node)
        return render_template(template_name, **ctx)
    except TemplateNotFound:
        return render_template('__404.html', **ctx)


@app.route('/__export/')
def export(page='/'):
    """
    Роут для экспорта всех темплейтов в самые тупы и обычные html файлы.
    Для всяких программистов, которые не могут осилить темплейты
    """

    result = ''
    export_dir = os.path.join(PATH, EXPORT_DIR)

    def __export_helper(files, export_dir):
        result = ''
        for f in files:
            # Проверяем, есть ли такая директория
            if not os.path.exists( export_dir ):
                os.mkdir( export_dir )

            # Если это внезапно папка - то рекурсивно пробегаемся по ней
            if f.isdir:
                result += __export_helper(f.files, os.path.join(export_dir, f.name))
                continue

            ctx = {}
            # extends
            if FIXTURE in ENABLE_EXTINSIONS:
                fixture = load_fixture(path=f.path)
                ctx.update(fixture)
            if TEMPLATE_LIST in ENABLE_EXTINSIONS:
                node = Node(True, TEMPLATE_DIR, '/',
                        __get_files( os.path.join(PATH, TEMPLATE_DIR)))
                ctx['templates'] = render_template('__files_list.html', node=node, is_export=True)
            export_template = render_template('%s.html' % f.path, **ctx)

            # Пытаемся экспортировать
            try:
                export_template_link = open(
                    os.path.join(export_dir, f.name), mode='wb')

                # Делаем относительный путь, чтобы не от корня считался, а от файлика
                relative_path = os.path.relpath(
                                    os.path.join(PATH, STATIC_DIR),
                                    os.path.join(PATH, export_dir) )\
                                    .replace('\\', '/')

                # Нагло реплейсим пути к статике прямо внутри шаблона
                # export_template = export_template.replace('/%s' % STATIC_DIR, relative_path)

                export_template_link.write( export_template.encode('utf-8') )
                export_template_link.close()

                # Пишем в лог, что все ок.
                result += 'export templates %s\n<br>' % f.path
            except IOError:
                # Если нет прав на запись или не можем найти папочку — эксептим
                result += '[!] export templates error: %s\n<br>' % f.path

        return result

    result += __export_helper(
        __get_files(os.path.join(PATH, TEMPLATE_DIR)),
        export_dir)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
