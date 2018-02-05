#!/usr/local/bin/python

import os
import sys
import cgi, cgitb
import psycopg2
import subprocess
import smtplib
from subprocess import PIPE, Popen

# Dump errors to browser
# cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
phase = form.getvalue('phase')
info = {}
for field in ['name', 'email', 'phone', 'class', 'comments', 'role']:
    info[field] = form.getvalue(field)

# Write data to file (just in case)
with open('signups.dat', 'a') as signups_file:
    signups_file.write('{}\n'.format(info))

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

        cursor.execute("INSERT INTO tblSignups (name,email,phone,class,role,comments,created) VALUES (%s,%s,%s,%s,%s,%s,now()) RETURNING id",
            (info['name'], info['email'], info['phone'], info['class'], info['role'], info['comments']))
        new_row = cursor.fetchone()
        if new_row is None:
            error = "Unable to save record to database"
        else:
            signup_id = new_row[0]
            if phase_id is not None:
                cursor.execute("INSERT INTO xrefSignupsPhases (signup_id, phase_id, created) VALUES (%s,%s,now())", (signup_id, phase_id))

# Send email
try:
    from_addr = '"Lip Dub MICDS Website" <www@libdubmicds.org>'
    to_addr = '"Sebastian Neumann" <sebastian@neumannfamily.net>'
    message = ''
    message += "From: {0}\n".format(from_addr)
    message += "To: {0}\n".format(to_addr)
    message += 'Subject: Lip Dub Signup\n\n'
    for field in ['name', 'email', 'phone', 'class', 'role', 'comments']:
        message += "{0}: {1}\n".format(field.capitalize(), info[field])
    s = smtplib.SMTP('localhost')
    s.sendmail(from_addr, to_addr.split(','), message)
    s.quit()
except:
    with open('errors.dat', 'a') as error_file:
        error_file.write('{0}\n'.format(sys.exc_info()[0]))

# Generate output
BASEDIR = '/usr/www/hosted/lipdubmicds'
SUBDIR = 'signup'
INPDIR = 'staging'
TEMPLATE = 'signup-template.html'

vars = []
vars.append('name=' + info['name'])
if error is not None: vars.append('error=true')

args = ['/usr/www/bin/template.pl', '-B:'+BASEDIR, '-C:'+SUBDIR, '-I:'+INPDIR, '-t:'+TEMPLATE, '-f:'+','.join(vars), 'thankyou.html']
session = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()

# Print output
print "Content-Type: text/html\r\n\r\n"
print stdout
