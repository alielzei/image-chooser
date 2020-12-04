import csv
import json
import sqlite3
import os 

from flask import Flask, render_template, request, send_file
app = Flask(__name__)

@app.route('/')
def main():
    f = open('list.csv')
    reader = csv.reader(f)
    next(reader)
    return render_template('index.html', diseases=[(row[0], row[1], row[4], row[3]) for row in reader])

@app.route('/disease/<int:id>', methods = ['GET', 'POST', 'DELETE'])
def disease(id):
    if request.method == "GET":
        f = open(f"source/{id}.dat")

        scriptdata = json.loads(f.read())
        images = scriptdata[31][0][12][2]

        result = []
        for image in images:
            try:
                lowres = image[1][2][0]
                hires = image[1][3][0]
                description = image[1][9]["2003"][3]

                result += [(id, lowres, hires, description)]
            except TypeError:
                pass

        return render_template('disease.html', images=result)

    if request.method == "POST":
        conn = sqlite3.connect('images.db')
        c = conn.cursor()

        data = [r for r in request.form.listvalues()]
        if(len(data)):
            data = data[0]
        for link in data:
            c.execute('insert or ignore into imageurls(id, url) values(?, ?)', (id, link))

        conn.commit()
        conn.close()


        return 'done'

@app.route('/images.db')
def database():
    return send_file('images.db', attachment_filename='images.db')