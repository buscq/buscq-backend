#!/usr/bin/python
# -*- coding: utf-8 -*-

endpoint_lines       = 'http://app.tussa.org/tussa/api/lineas'
endpoint_stop        = 'http://app.tussa.org/tussa/api/paradas/'

lines_and_stops      = 1
times                = 2
update_all           = 3

mySQL_host           = 'localhost'
mySQL_user           = 'root'
mySQL_db             = 'buscq'

populate_lines_query = """INSERT INTO `lines` (id, line, name, color)
                          VALUES (%(id)s, %(line)s, %(name)s, %(color)s)
                          ON DUPLICATE KEY UPDATE
                              line  = CASE WHEN VALUES(line) <> line
                                         THEN VALUES(line)
                                         ELSE line
                                      END
                            , name  = CASE WHEN VALUES(name) <> name
                                         THEN VALUES(name)
                                         ELSE name
                                      END
                            , color = CASE WHEN VALUES(color) <> color
                                         THEN VALUES(color)
                                         ELSE color
                                      END
                       """

populate_stops_query = """INSERT INTO `stops` (id, name, zone, lat, lon, extra)
                          VALUES (%(id)s, %(name)s, %(zone)s, %(lat)s, %(lon)s, %(extra)s)
                          ON DUPLICATE KEY UPDATE
                              name  = CASE WHEN VALUES(name) <> name
                                         THEN VALUES(name)
                                         ELSE name
                                      END
                            , zone  = CASE WHEN VALUES(zone) <> zone
                                         THEN VALUES(zone)
                                         ELSE zone
                                      END
                            , lat   = CASE WHEN VALUES(lat) <> lat
                                         THEN VALUES(lat)
                                         ELSE lat
                                      END
                            , lon   = CASE WHEN VALUES(lon) <> lon
                                         THEN VALUES(lon)
                                         ELSE lon
                                      END
                            , extra = CASE WHEN VALUES(extra) <> extra
                                         THEN VALUES(extra)
                                         else extra
                                      END
                       """

select_stops_query = "SELECT id from `stops`"
update_times_query = """INSERT INTO `times` (stopId, line, name, nextBus, deltaBus, timestamp)
                        VALUES (%(stopId)s, %(line)s, %(name)s, %(nextBus)s, %(deltaBus)s, %(timestamp)s)
                     """
truncate_times     = "TRUNCATE TABLE `times`"
line_stops_query   = """INSERT INTO `lineStops` (lineId, stops0, stops1, isCircular)
                        VALUES (%(lineId)s, %(stops0)s, %(stops1)s, %(isCircular)s)"""
