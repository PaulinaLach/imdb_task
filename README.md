# IMDB task

## Requirements

Consider using virtualenv.

1. `pip install -r requirements.txt`
1. `manage.py migrate`

Database configuration is inside imdb/settings.py file.

By default it uses `imdb` database with trust authentication (only for development purposes).

## Running TSV importer

`manage.py tsv_importer --titles_path ./titles.tsv --names_path ./names.tsv` (--titles_path and --names_path are optional, default: <project_root>/titles.tsv and <project_root>/names.tsv)

File is in api/management/commands/tsv_importer.py

## Running web server

`manage.py runserver`

## API

There are two JSON endpoints:
 * GET /titles/ - lists titles in alphabetical order along with connected names
  with optional query params:
   * startYear - filters titles with given startYear
   * genre - filters titles that in genres array have given genre
 * GET /names/ - lists names with knownFor titles
 with optional query param:
   * name - filters names that match given name
