#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys

from jinja2 import Environment, FileSystemLoader


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
            talks.append(data)
        return talks



if __name__ == "__main__":

    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('acceptance.j2')

    data = load_csv()
    for talk in data:
        if talk['type'] == '30 minute':
            print template.render(talk=talk)
            print
            print
            print '#'
            print
