# Type checking your Django code with `django-types` and `pyright`

A talk given at [DjangoCon 2022 San Diego](https://2022.djangocon.us/). Code in this repo, [slides here](https://docs.google.com/presentation/d/1CoehhgRtjfTYHC_2rs_vmp9OcZHuKv2N5WGGULhpc8w).

Blurb: I work at [Elementary ML](https://www.elementaryml.com/). Check out our site, if it looks cool and you like writing code in Python [get in touch](https://elementary.bamboohr.com/jobs/).

## Abstract

By now most of us have heard of, or used, Python type hints. Since being added to Python in 3.5, they've spread to every corner of the Python ecosystem.

These days many libraries are built from the ground up with type hints. But type hints don't have to live inline with the code, or even in the same repo. Anyone can write standalone type hints (also called stubs) for a framework like Django, and eventually people did.

In this talk I'll show you how to use a great set of type stubs for Django called [django-types](https://github.com/sbdchd/django-types), how to check your type hints with [pyright](https://github.com/microsoft/pyright), some of the challenges with adding type hints to Django code, and how to make type hints and type checking a real productivity boost.

- A brief history of Django type stubs
- Which type stubs, and which type checker: `django-stubs` or `django-types`, `mypy` or `pyright`?
- Starting a project with type hints, or adding type hints to an existing project
- Where to focus: adding type hints to Django models and views
- Workarounds for when the type stubs aren't quite right
- Configuring `pyright` for type checking: running `pyright` on the host, in a container, on a CI server
- `pyright` and LSP clients: turning your text editor (Vim, Emacs, Sublime Text, VS Code, etc) into a full-fledged Python/Django IDE
- Type hints for documentation, code navigation, and refactoring

## Installing project deps and `pyright`

- Install [pyright](https://github.com/microsoft/pyright#installation), and enable pyright for your text editor
- Install [poetry](https://github.com/python-poetry/poetry)
- From the root of this repo, run `poetry install`
- Run `cp pyrightconfig-ci.json pyrightconfig.json`
- Run `poetry show -v`
- Open `pyrightconfig.json`, add the following lines with the virtualenv returned by `poetry show -v`

```json
"venvPath": ".../pypoetry/virtualenvs",
"venv": "django-types-talk-..."
```

## Code

We'll add type hints to the following data model, and add some type-hinted views that use these models.

```mmd
erDiagram
    user {
        id int
        email string
    }

    post {
        id int
        user_id int FK
        thread_id int FK
        text string
        is_deleted boolean
    }

    thread {
        id int
        moderator_id int FK
        name string
        meta json
    }

    post }|--|| user : ""
    post }|--|| thread : ""
    
    thread }|..|| user : "moderator"
    
    user }|--|{ thread : "subscribed_to"
```

### Django type hints recipes

We use [pyright](https://github.com/microsoft/pyright) for type checking, plus the dev improvements afforded by the pyright [language server](https://microsoft.github.io/language-server-protocol/).

We use type stub libraries for [Django](https://github.com/sbdchd/django-types) and [DRF](https://github.com/sbdchd/djangorestframework-types).

For Django, most type annotations go in **models** and **views**. For models, type annotations need to be added for:

- Foreign key `_id` fields, e.g. `moderator_id: uuid.UUID | None`
- Reverse foreign key managers, e.g. `posts: Manager[Post]`
- Many to many fields, e.g. `threads: models.ManyToManyField[Thread, UserThread]`
- Some rare special cases

If you need to import a model without causing a circular import issue, you can do so using the `TYPE_CHECKING` variable, which is `True` when checking types and `False` otherwise:

```py
if TYPE_CHECKING:
    from app.models import Post
```

In views, the most important thing is to type `request` as `UserRequest`, so `request.user` is typed as our `User` class, not one of Django's built-in user classes.

You can read the [django-types docs](https://github.com/sbdchd/django-types) or look at code in this code base to get a better idea.

If you need to work around or ignore a type error, use `cast`, `not_none`, or the `# type: ignore` comment.

## Prior art

- https://github.com/typeddjango/django-stubs
    - The library from which https://github.com/sbdchd/django-types was forked
- https://kracekumar.com/post/type_check_your_django_app/
    - A presentation from PyCon India 2021 on using `django-stubs`, which unfortunately aren't compatible with any type checker other than `mypy`

There's an [open issue in django-stubs](https://github.com/typeddjango/django-stubs/issues/579) to make them compatible with `pyright`.
