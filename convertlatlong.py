import csv
import argparse
import datetime
import pytz
from timezonefinderL import TimezoneFinder
from pytz import timezone 

DEFAULT_TERM = 1480042675
DEFAULT_LONGITUDE = 122.41
DEFAULT_LATITUDE = -37.76
tf = TimezoneFinder()

def main():
    print(TimezoneFinder.using_numba())
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--utc', dest='utc', default=DEFAULT_TERM,
                        type=float, help='Search term (default: %(default)s)')
    parser.add_argument('-lon', '--longitude', dest='lon',
			default=DEFAULT_LONGITUDE, type=float,
			help='Search longitude (default: %(default)f)')
    parser.add_argument('-lat', '--latitude', dest='lat',
                        default=DEFAULT_LATITUDE, type=float,
                        help='Search latitude (default: %(default)f')

    input_values = parser.parse_args()

    try:
        query_local(input_values.lat, input_values.lon, input_values.utc)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    with open('11_16_US_Thanksgiving.csv') as csvfile:
        zipreader = csv.reader(csvfile)
        flag = False
        count = 0
        with open('output.csv','w',newline='') as csvout:
            for row in zipreader:
                count = count + 1
                if count == 10:
                    exit
                if flag is False:
                    flag = True
                    continue
                lat = float(row[3])
                lon = float(row[4])
                utcTim = int(row[0])
                aware_time = query_local(lat, lon, utcTim)
                write_row=list(row)
                write_row.append(str(aware_time))
                spamwriter = csv.writer(csvout)
                spamwriter.writerow(write_row)

def query_local(latitude, longitude, utcTime):
    
    aware_datetime_in_local = datetime.datetime.now
    try:
        timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
        if(timezone_name is None or timezone_name is 'uninhabited'):
            print(timezone_name)
            timezone_name = tf.closest_timezone_at(lng=longitude, lat=latitude)
        if(timezone_name is not 'uninhabited'):
            tz = timezone(timezone_name)
            value = datetime.datetime.fromtimestamp(utcTime)
            aware_datetime = pytz.utc.localize(value)
            aware_datetime_in_local = aware_datetime.astimezone(tz)
    except RuntimeWarning:
        pass
    return aware_datetime_in_local

if __name__ == '__main__':
    main()
