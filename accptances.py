#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016 IBM
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# If updating the puppet system-config repo or installing puppet modules
# fails then abort the puppet run as we will not get the results we
# expect.

import config

import csv
import sys

import os
import re

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText


from jinja2 import Environment, FileSystemLoader

SMTPserver = 'mail.messagingengine.com'
sender =     'DevOpsDays Portland Organizers <nibz+devopsdays@spencerkrum.com>'

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'





def load_csv(filename='accepted.csv'):
    print "Whoo loading data from file {0}:".format(filename)
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        talks = []
        for row in reader:
            data = {}
            data['speaker'] = row['speaker 1: first_name']
            data['title'] = row['title']
            data['bio'] = row['speaker 1: bio']
            data['description'] = row['description']
            data['type'] = row['What length of talk is this?']
            data['email'] = row['speaker 1: email']
            talks.append(data)
        return talks



if __name__ == "__main__":

    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('acceptance.j2')

    data = load_csv()
    for talk in data:
        if talk['type'] == '30 minute':
            print "To: {0}".format(talk['email'])
            content = template.render(talk=talk)
            destination = [talk['email'], 'organizers-portland-2016@devopsdays.org']
            subject="Congratulations, we want you to speak at DevOpsDays Portland!"
            try:
                msg = MIMEText(content, text_subtype)
                msg['Subject']=       subject
                msg['To'] = talk['email']
                msg['From']   = sender # some SMTP servers will do this automatically, not all
                msg['Cc'] = 'organizers-portland-2016@devopsdays.org'
                msg['Reply-To'] = 'organizers-portland-2016@devopsdays.org'

                conn = SMTP(SMTPserver)
                conn.set_debuglevel(False)
                conn.login(config.USERNAME, config.PASSWORD)
                try:

                    conn.sendmail(sender, destination, msg.as_string())
                    print sender, destination, msg.as_string()
                finally:
                    conn.quit()

            except Exception, exc:
                sys.exit( "mail failed; %s" % str(exc) ) # give a error message
