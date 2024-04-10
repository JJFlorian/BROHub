# BROStar API


## Introduction

BROStar is a data management product for the Dutch *Basis Registratie Ondergrond* (BRO). The code for the backend is stored in this repository. It consists of an API for importing, storing, and delivering data. The backend is open source, and can be self-hosted. The frontend is developed and hosted by Nelen & Schuurmans. This is a web application created on top of the API, making the data management of BRO data very accessible. Interested? Contact [info@nelen-schuurmans.nl](mailto:info@nelen-schuurmans.nl).


## Project description

The backend consists of an API with:

- An import task endpoint. This can import all current data from a BRO domain based on a KvK and project number.

- An upload task endpoint. This can send data to the BRO, with a JSON input of all relevant data. The API handles the transformation to XML format and the message traffic to and from the BRO.

- Endpoints for all assets imported from the BRO.

## Backend development instructions

To install for development:

    $ docker-compose build
    $ docker-compose pull
    $ pip install pre-commit  # Just needed once for your laptop.

The development setup includes a postgres database and redis.

Some instructions:

    $ docker-compose up  # Starts the site on localhost:8000
    $ docker-compose run --rm web pytest
    $ docker-compose run --rm web python manage.py migrate
    $ pre-commit run --all  # runs the formatter, checks, etc.

Do the regular django "migrate", "createsuperuser" stuff.

7) Create an organization, fill in the KvK, and optionally fill in authentication details.

8) Create a user profile for the superuser.

If a requirement has changed (either dependency in `pyproject.toml` or an extra development package in `requirements.in`:

    $ docker-compose run --rm web pip-compile
    $ docker-compose run --rm web pip-compile --upgrade  # to grab new versions


## Internal N&S server installation notes

This is a public project, so the actual server deployment scripts with the passwords and so are safely hidden away in https://github.com/nens/brostar-site :-) We're installed with docker-compose on https://staging.brostar.nl and https://www.brostar.nl . See the readme of `brostar-site` for the internal deployment documentation.
