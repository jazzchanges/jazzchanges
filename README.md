# Jazzchanges Django Project #
## Prerequisites ##

- python >= 2.5
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python enviroment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```mkvirtualenv --no-site-packages jazzchanges-env```

#### For virtualenv ####
```virtualenv --no-site-packages jazzchanges-env```

```cd jazzchanges-env```

```source bin/activate```

### Clone the code ###
Obtain the url to your git repository.
```git clone https://github.com/bryanhelmig/jazzchanges jazzchanges```

### Install requirements ###
```cd jazzchanges```

```pip install -r requirements.txt```

### Configure project ###
```cp jazzchanges/__local_settings.py jazzchanges/local_settings.py```

```vi jazzchanges/local_settings.py```

### Sync databases & migrate ###
```python manage.py syncdb```
```python manage.py migrate```

## Running ##
```python manage.py runserver```

Open browser to 127.0.0.1:8000