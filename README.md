# Eventex

Project developed during the [WTTD](http://welcometothedjango.com.br)

[![Build Status](https://travis-ci.org/cuducos/wttd-eventex.svg?branch=master)](https://travis-ci.org/cuducos/wttd-eventex)
[![Code Climate](https://codeclimate.com/github/cuducos/wttd-eventex/badges/gpa.svg)](https://codeclimate.com/github/cuducos/wttd-eventex)


## Running locally

1. Clone the repository
2. Create a virtualenv with Python 3.5
3. Activate the virtualenv
4. Install the dependencies
5. Set up your local configuration file
6. Run tests

```console
git clone git@github.com:cuducos/wttd-eventex.git wttd && cd wttd
python -m venv .wttd
source .wttd/bin/activate
python -m pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Deploying with Heroku

1. Create a Heroku app
2. Send your configuration variables to Heroku
3. Define a _secret key_
4. Disable _debug_ mode
5. Set up the mail service
6. Push your code

```console
heroku create your_name-eventex
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# config your email according to your provider settings
git push heroku master

```
