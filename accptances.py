#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys

from jinja2 import Environment, FileSystemLoader


def load_csv(filename='accepted.csv'):
    print "Whoo loading data from file {0}:".format(filename)
    with open(filename, 'rb') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',')
        talks = []
        for row in csvdata:
            data = {}
            data['speaker'] = row[24] + ' ' + row[25]
            data['title'] = row[1]
            data['bio'] = row[29]
            data['description'] = row[2]
            talks.append(data)
        return talks


if __name__ == "__main__":

    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('acceptance.j2')

    data = load_csv()
    for talk in data:
        print template.render(talk=talk)
        print
        print
        print '#'
        print
