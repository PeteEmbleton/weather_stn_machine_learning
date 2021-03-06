#!/usr/bin/env python3

#this script shoudl run every 3 mins
#it will query the latest infromation and insert it ito the MYsql
# matches based upon weather_stn IDS and timestamp so you dont get duplicates


import urllib.request, json, MySQLdb
from dateutil.parser import parse

counter = 0 # intialise a counter
db =MySQLdb.connect(host="127.0.0.1",
                    port=3306, # your host, usually localhost
                    user="<username>",         # your username
                    passwd="<password>",  # your password
                    db="weather_stn")        # name of the data base
cursor = db.cursor()

update_record = ("INSERT INTO weather_stn "
                 "(weather_stn_id, ambient_temp, ground_temp, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall, reading_timestamp) " #,created_by,created_on,updated_by,updated_on) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)") #, %(createdby)s, %(created_on)s, %(updated_by)s, %(updated_on)s)")


with urllib.request.urlopen("https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement") as url:
    all_stations = json.loads(url.read().decode())
    next_url = all_stations['next']['$ref'] #get the next url

    for i in range(len(all_stations['items'])):
        continue_loop = 1
        #need to try all the fields as some may be missing
        stn_id = (all_stations['items'][i]['weather_stn_id'])
        try:
            stn_id = (all_stations['items'][i]['weather_stn_id'])
        except:
            pass
        else:
            stn_id = (all_stations['items'][i]['weather_stn_id'])

        try:
            ambient_temp = (all_stations['items'][i]['ambient_temp'])
        except:
            pass
        else:
            ambient_temp = (all_stations['items'][i]['ambient_temp'])

        try:
            ground_temp = (all_stations['items'][i]['ground_temp'])
        except:
            pass
        else:
            ground_temp = (all_stations['items'][i]['ground_temp'])

        try:
            air_quality = (all_stations['items'][i]['air_quality'])
        except:
            pass
        else:
            air_quality = (all_stations['items'][i]['air_quality'])

        try:
            air_pressure = (all_stations['items'][i]['air_pressure'])
        except:
            pass
        else:
            air_pressure = (all_stations['items'][i]['air_pressure'])

        try:
            humidity = (all_stations['items'][i]['humidity'])
        except:
            pass
        else:
            humidity = (all_stations['items'][i]['humidity'])

        try:
            wind_direction = (all_stations['items'][i]['wind_direction'])
        except:
            pass
        else:
            wind_direction = (all_stations['items'][i]['wind_direction'])

        try:
            wind_speed = (all_stations['items'][i]['wind_speed'])
        except:
            pass
        else:
            wind_speed = (all_stations['items'][i]['wind_speed'])

        try:
            wind_gust_speed = (all_stations['items'][i]['wind_gust_speed'])
        except:
            pass
        else:
            wind_gust_speed = (all_stations['items'][i]['wind_gust_speed'])

        try:
            rainfall = (all_stations['items'][i]['rainfall'])
        except:
            pass
        else:
            rainfall = (all_stations['items'][i]['rainfall'])

        try:
            time_to_convert = str(all_stations['items'][i]['reading_timestamp'])
            reading_timestamp = str((parse(time_to_convert))).split('+', 1)[0]

        except:
            pass
        else:
           time_to_convert = str(all_stations['items'][i]['reading_timestamp'])
           reading_timestamp = str((parse(time_to_convert))).split('+', 1)[0]


        #print(stn_id, reading_timestamp)
        data_exists = (cursor.execute("""SELECT reading_timestamp FROM weather_stn WHERE weather_stn_id = '%s' and reading_timestamp = '%s'""" %(stn_id,reading_timestamp)))
        #print(data_exists)

        if data_exists == 0:
            stn_data = (stn_id, ambient_temp, ground_temp, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall, reading_timestamp)
            cursor.execute(update_record, stn_data)
            db.commit()

            counter += 1
            #print("create record")


            while continue_loop == 1:
                try:
                    with urllib.request.urlopen(next_url) as url:
                        station_data_next = json.loads(url.read().decode())
                        next_url = station_data_next['next']['$ref']

                except KeyError:
                    continue_loop = 0
                else:
                    #print(next_url)
                    with urllib.request.urlopen(next_url) as url:
                        station_data = json.loads(url.read().decode())

                        for k in range(len(station_data['items'])):
                            #need to try all th fields as some may be missing

                            try:
                                stn_id = (station_data['items'][k]['weather_stn_id'])
                            except:
                                pass
                            else:
                                stn_id = (station_data['items'][k]['weather_stn_id'])

                            try:
                                ambient_temp = (station_data['items'][k]['ambient_temp'])
                            except:
                                pass
                            else:
                                ambient_temp = (station_data['items'][k]['ambient_temp'])

                            try:
                                ground_temp = (station_data['items'][k]['ground_temp'])
                            except:
                                pass
                            else:
                                ground_temp = (station_data['items'][k]['ground_temp'])

                            try:
                                air_quality = (station_data['items'][k]['air_quality'])
                            except:
                                pass
                            else:
                                air_quality = (station_data['items'][k]['air_quality'])

                            try:
                                air_pressure = (station_data['items'][k]['air_pressure'])
                            except:
                                pass
                            else:
                                air_pressure = (station_data['items'][k]['air_pressure'])

                            try:
                                humidity = (station_data['items'][k]['humidity'])
                            except:
                                pass
                            else:
                                humidity = (station_data['items'][k]['humidity'])

                            try:
                                wind_direction = (station_data['items'][k]['wind_direction'])
                            except:
                                pass
                            else:
                                wind_direction = (station_data['items'][k]['wind_direction'])

                            try:
                                wind_speed = (station_data['items'][k]['wind_speed'])
                            except:
                                pass
                            else:
                                wind_speed = (station_data['items'][k]['wind_speed'])

                            try:
                                wind_gust_speed = (station_data['items'][k]['wind_gust_speed'])
                            except:
                                pass
                            else:
                                wind_gust_speed = (station_data['items'][k]['wind_gust_speed'])

                            try:
                                rainfall = (station_data['items'][k]['rainfall'])
                            except:
                                pass
                            else:
                                rainfall = (station_data['items'][k]['rainfall'])

                            try:
                                time_to_convert = str(all_stations['items'][k]['reading_timestamp'])
                                reading_timestamp = str((parse(time_to_convert))).split('+', 1)[0]
                            except:
                                pass
                            else:
                                time_to_convert = str(all_stations['items'][i]['reading_timestamp'])
                                reading_timestamp = str((parse(time_to_convert))).split('+', 1)[0]

                            stn_id = (station_data['items'][k]['weather_stn_id'])


                            #print(stn_id, reading_timestamp)
                            data_exists = (cursor.execute("""SELECT reading_timestamp FROM weather_stn WHERE weather_stn_id = '%s' and reading_timestamp = '%s'""" %(stn_id,reading_timestamp)))
                            #print(data_exists)

                            if data_exists == 0:
                                stn_data = (stn_id, ambient_temp, ground_temp, air_quality, air_pressure, humidity, wind_direction, wind_speed, wind_gust_speed, rainfall, reading_timestamp)
                                cursor.execute(update_record, stn_data)
                                db.commit()
                                counter += 1
                                print("create record")

    cursor.close()
    db.close()
print("updated ",counter)

