# makeup-workflow

Каркас для верстки на базе [Flask](http://flask.pocoo.org/) и [Jinja](http://jinja.pocoo.org/).

## Описание
Каркас реализован на микрофреймоврке [Flask](http://flask.pocoo.org/)/Python, который любезно предоставляет
роутинг и оберту для шаблонизатора [Jinja](http://jinja.pocoo.org/). Концепция позаимствована у хабрпользователя
[magic4x](http://habrahabr.ru/post/164823/).

Собственно, нынетрендовый, декларативный стиль верстки — это, безусловно, очень круто, но не им едины, и «по-старинке»
иной раз лучше и проще. Особенно, когда мы избавляемся от необходимости копипастить шапку, подвал в каждом шаблоне, а
пользуемся привычными и удобными, созданными для этих целей, шаблонизаторами, в нашем случае — Jinja.

Это небольшое приложение поможет вам верстать, используя шаблонизатор, избавляя, тем самым, от надуного
копипаста, и даруя все возможности шаблонизатора. Сразу вшит бутстрап, и несколько дополнительных вкусняшек.
Используется в качестве базовго шаблона.

## Установка и использование

Подразумевается, что python, setuptools и pip уже стоят. Если нет, то вы сами лучше знаете, как их поставить
на вашей платформе.

```
pip install virtualenvwrapper
mkvirtualenv flask-env
pip install flask
cd PROJECT_DIR_WITH_APP
./app.py
```

Наш flask-сервер повиснет по адресу `http://127.0.0.1:5000/` и там его можно увидеть в браузере.

## Workflow
Наши шаблоны находятся в директории `./templates`. Есть определенное соглашение, в рамках которого шаблоны,
которые начинаются с `__` являются системными: это или базовые, или импортируемые блоки.

В качестве примера, создан один пустой шаблон `index.html`. Все повторяющиеся элементы мы можем свободно описать в
`base.html`, контент зона описывается внутри блока `{% block content %}...{% endblock %}`. Впоследствии, этот шаблон
будет доступен по адресу `http://127.0.0.1:5000/index/`. Если вам нужно посмотреть все шаблоны, которые есть у вас в
проекте, они перечислены на индексной странице `http://127.0.0.1:5000/`. Так же, поддерживаются поддиректории.
Все, что вам нужно еще — синтакси Jinja.

## Экспорт шаблонов
Бывают ситуации, когда по каким-то причинам, вы не располгаете возможностью запустить сервер, а шаблоны нужны.
Например: необходимо продемонстрировать плоды работы менеджеру или клиенту, или программист по каким-то ему одному
понятным соображениям отказывается принимать вменяемые шаблоны на Jinja и требует привычную html-помойку кода, вы
можете "склеить" все шаблоны в обычные html-файлы. Все, что вам нужно, это набрать в браузере

```
http://127.0.0.1:5000/__export/
```

# Расширения

## fixture
Расширение, которое реализует подгрузку контента из json
Использование:
a) Использование сквозных фикстур:
    Фикстуры, которые должны присутствовать на всех страницах
    определяются в файле `fixture/__base.json`
б) Фикстуры для определенных страниц:
    В директроии fixture/ создаем файл, одноименный с названием
    страницы, на которую фикстура должна подгружаться 
    (для файла `templates/foo_bar.html` создаем фикстуру `fixture/foo_bar.json`)
Использование в шаблоне:
    Фикстуры автоматически подгружаются в контекст, далее в шаблоне используются 
    привычными способами. (`{{ variable }}`)

## template list
Расширение, которое добавляет в отрендеренную страницу список остальных страниц


# Используемая литература
* [Jinja](http://jinja.pocoo.org/)
* [Flask](http://flask.pocoo.org/)
* [Python](http://www.python.org/)
* [Bootstrap](http://twitter.github.com/bootstrap/)