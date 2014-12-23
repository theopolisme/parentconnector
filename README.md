parentconnector
===============

An unofficial API for Pearson's ParentCONNECTxp, providing programmatic access to grades and student information.

## Usage

Either use `parentconnector.py` as a standalone script, or use the entire repository as a basic Flask-app-turned-web-API extravaganza, with `wsgi.py` as the web endpoint. 

### Standalone

```
usage: parentconnector.py [-h] base_url username password

positional arguments:
  base_url    base url of the ParentConnect instance, including protocol and
              trailing slash
  username    username (typically email address) of the user to log in as
  password    password of the user to log in as
```

## Dependencies & courtesies

```
beautifulsoup4==4.3.2
Flask==0.10.1
Flask-SSLify==0.1.4
itsdangerous==0.24
Jinja2==2.7.3
MarkupSafe==0.23
requests==2.5.1
selenium==2.44.0
virtualenv==12.0.2
Werkzeug==0.9.6
```

* `parentconnector` also requires `phantomjs` to be installed.

* The API page incorporates design elements from [earwig/copyvios](https://github.com/earwig/copyvios) by Ben Kurtovic. 

## License

Copyright (C) 2014 Theo Patt <theo@theopatt.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
