#!/usr/local/bin/python

import os
import cgi, cgitb
import tempfile
import psycopg2
import subprocess
from subprocess import PIPE, Popen

# Dump errors to browser
cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
phase = form.getvalue('phase')
info = {}
for field in ['name', 'email', 'phone', 'class']:
    info[field] = form.getvalue(field)
info['assistant'] = True if form.getvalue('assistant', '') != '' else False

# Connect to database
session = subprocess.Popen(['/usr/www/bin/read_dbcfg', 'lipdubmicds'], stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()
d = {}
for pair in stdout.split(' '):
    f, v = pair.split('=')
    d[f] = v

conn_string = "host='localhost' dbname='{0}' user='{1}' password='{2}'".format(d['db'], d['u'], d['passwd'])
conn = psycopg2.connect(conn_string)

# Insert records into database
error = None
with conn:
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM tblPhases WHERE phase=%s', (phase,))
        row = cursor.fetchone()
        phase_id = None
        if row is not None:
            phase_id = row[0]

        cursor.execute("INSERT INTO tblSignups (name,email,phone,class,created) VALUES (%s,%s,%s,%s,now()) RETURNING id",
            (info['name'], info['email'], info['phone'], info['class']))
        new_row = cursor.fetchone()
        if new_row is None:
            error = "Unable to save record to database"
        else:
            signup_id = new_row[0]
            if phase_id is not None:
                cursor.execute("INSERT INTO xrefSignupsPhases (signup_id, phase_id, created) VALUES (%s,%s,now())", (signup_id, phase_id))

# Format output
if error is None:
    text = '''
    <h2>Submitted Info</h2>
    <table>
    <tr><th>Name</th><td>{name}</td></tr>
    <tr><th>Email</th><td>{email}</td></tr>
    <tr><th>Phone</th><td>{phone}</td></tr>
    <tr><th>Class</th><td>{class}</td></tr>
    <tr><th>Assistant?</th><td>{assistant}</td></tr>
    </table>
    '''.format(**info)
else:
    text = error

# Generate output
BASEDIR = '/usr/www/hosted/lipdubmicds'
SUBDIR = 'signup'
INPDIR = 'staging'
TEMPLATE = 'signup-template.html'
TMPNAME = next(tempfile._get_candidate_names()) + '.html'
ofname = '{0}/{1}/{2}/{3}'.format(BASEDIR, INPDIR, SUBDIR, TMPNAME)
with open(ofname, 'w') as ofile: ofile.write(text)

args = ['/usr/www/bin/template.pl', '-B:'+BASEDIR, '-C:'+SUBDIR, '-I:'+INPDIR, '-t:'+TEMPLATE, '-f:name='+info['name'], 'thankyou.html']
session = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()
os.remove(ofname)

# Print output
print "Content-Type: text/html\r\n\r\n"
print stdout
