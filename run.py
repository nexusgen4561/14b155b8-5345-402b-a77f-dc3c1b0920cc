# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

app = Flask(__name__, template_folder='templates')

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG           =' + str(DEBUG))
    app.logger.info('Page Compression=' + 'FALSE' if DEBUG else 'TRUE')
    app.logger.info('DBMS            =' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT     =' + app_config.ASSETS_ROOT)


@app.route("/")
@app.route("/policies.html")
def index():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from Policies")
    data = cur.fetchall()
    return render_template('home/policies.html', datas=data)


@app.route("/add_policy", methods=['POST', 'GET'])
def add_policy():
    if request.method == 'POST':
        date = request.form['date']
        code = request.form['code']
        name = request.form['name']
        cost = request.form['cost']
        duration = request.form['duration']
        status = request.form['status']
        document = request.form['document']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        # cur.execute("insert into users(UNAME,CONTACT) values (?,?)",(uname,contact))
        cur.execute("insert into Policies(Date_Created, Policy_Code, Policy_Name, Policy_Cost, Duration, Status, Document) values (?,?,?,?,?,?,?)",
                    (date, code, name, cost, duration, status, document))
        con.commit()
        flash('Policy Added', 'success')
        return redirect(url_for("index"))
    return render_template("/home/add_policy.html")


@app.route("/edit_policy/<string:uid>", methods=['POST', 'GET'])
def edit_policy(uid):
    if request.method == 'POST':
        date = request.form['date']
        code = request.form['code']
        name = request.form['name']
        cost = request.form['cost']
        duration = request.form['duration']
        status = request.form['status']
        document = request.form['document']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("update Policies set DateCreated=?,Policy_Code=?,Policy_Name=?,Policy_Cost=?,Duration=?,Status=?,Document=? where UID=?",
                    (date, code, name, cost, duration, status, document, uid))
        con.commit()
        flash('Policy Updated', 'success')
        return redirect(url_for("index"))
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from Policies where ID=?", (uid,))
    data = cur.fetchone()
    return render_template("/home/edit_policy.html", datas=data)


@app.route("/delete_policy/<string:uid>", methods=['GET'])
def delete_policy(uid):
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("delete from Policies where ID=?", (uid,))
    con.commit()
    flash('Policy Deleted', 'warning')
    return redirect(url_for("index"))

# Feedback Churn


@app.route("/")
@app.route("/churn_forms.html")
def churn():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from feedbacks")
    data = cur.fetchall()
    return render_template('home/churn_forms.html', datas=data)


@app.route("/churn_forms", methods=['POST', 'GET'])
def churn_forms():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        prev_sub = request.form['prev_sub']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        q8 = request.form['q8']
        q9 = request.form['q9']
        q10 = request.form['q10']
        q11 = request.form['q11']
        q12 = request.form['q12']
        q13 = request.form['q13']
        reason = request.form['reason']
        comment = request.form['comment']
        date_added = date("Y-m-d H:i:s")
        con = sql.connect("db_web.db")
        cur = con.cursor()
        # cur.execute("insert into users(UNAME,CONTACT) values (?,?)",(uname,contact))
        cur.execute("insert into feedbacks (name, age, gender, email, prev_sub, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, reason, comment, date_added, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, age, gender, email, prev_sub, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, reason, comment, date_added))
        con.commit()
        flash('Feedback Submitted', 'success')
        return redirect(url_for("churn"))
    return render_template("/home/churn_forms.html")


if __name__ == "__main__":
    app.run()
