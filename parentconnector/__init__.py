# -*- coding: utf-8 -*-

"""
__init__.py
========

The ParentConnector web API endpoint

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
"""

import os
import time
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sslify import SSLify
from parentconnector import ParentConnector

app = Flask(__name__)
sslify = SSLify(app)

app.config['PHANTOMJS_PATH'] = os.environ.get('PHANTOMJS_PATH', 'phantomjs')

def make_api_error(error):
    return jsonify(success=False, message=error), 500

@app.errorhandler(404)
def page_not_found(ex):
    return redirect(url_for('api'))

@app.route('/api.json', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return render_template('api.html')

    start_time = time.time()

    action = request.form.get('action')
    base_url = request.form.get('base_url')
    username = request.form.get('username')
    password = request.form.get('password')

    if action not in ['assignments', 'students']:
        return make_api_error('Invalid action: Action must be "assignment" or "students".')

    if not username:
        return make_api_error('Invalid username: No username specified.')

    if not password:
        return make_api_error('Invalid password: No password specified.')

    connector = ParentConnector(base_url, username, password, app.config['PHANTOMJS_PATH'])

    connector.login()
    if not connector.is_logged_in:
        return make_api_error('Login error: Invalid credentials, or the server may be down.')        

    if action == 'students':
        result = connector.get_students()
    elif action == 'assignments':
        result = connector.get_assignments(student_index=request.form.get('student_index'))

    response = jsonify({
        'success': True,
        'elapsed': time.time() - start_time,
        action: result
    })

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run()
