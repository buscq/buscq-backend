#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import time

import MySQLdb

from var import *

db = MySQLdb.connect(host = mySQL_host, user = mySQL_user, db = mySQL_db, charset = 'utf8')
cur = db.cursor()

def update_lines_and_stops():
    """Fetches and inserts all bus data into the database."""
    lines_json = json.loads(requests.get(endpoint_lines).text)
    lol = 0
    for i in lines_json:
        data_line = {
            'id':    i['codigo'],
            'line':  i['sinoptico'],
            'name':  i['nombre'],
            'color': i['estilo']

            }
        cur.execute(populate_lines_query, data_line)
        db.commit()

        line_json = json.loads(requests.get(endpoint_lines + '/' + i['codigo']).text)

        for z in line_json['trayectos']:
            stops_temp = ''
            for v in z['paradas']:
                stops_temp += v['codigo'] + ', '
                data_stops = {
                    'id':    v['codigo'],
                    'name':  v['nombre'],
                    'zone':  v['zona'],
                    'lat':   v['coordenadas']['latitud'],
                    'lon':   v['coordenadas']['longitud'],
                    'extra': v['extraordinaria']
                }
            line_stops = {'lineId': i['codigo']}
            line_stops.update({'stops0' if z['sentido'] == 'IDA' else 'stops1': stops_temp})

            cur.execute(populate_stops_query, data_stops)
            db.commit()

def update_times():
    cur.execute(truncate_times)
    db.commit()

    cur.execute(select_stops_query)
    for row in cur.fetchall():
        stop_json = json.loads(requests.get(endpoint_stop + str(row[0])).text)
        for i in stop_json['lineas']:
            data_times = {
                'stopId':    row[0],
                'line':      i['sinoptico'],
                'name':      i['nombre'],
                'nextBus':   i['proximoPaso'],
                'deltaBus':  i['minutosProximoPaso'],
                'timestamp': int(time.time())
            }

            cur.execute(update_times_query, data_times)
            db.commit()


def populate_db():
    if category == lines_and_stops:
        update_lines_and_stops()
    elif category == times:
        update_times()
    elif category == update_all:
        update_lines_and_stops()
        update_times()
    else:
        raise ValueError(str(times) + ' is not a valid category.')

update_lines_and_stops()
