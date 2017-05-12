import csv
import argparse
import datetime
import pytz
from timezonefinderL import TimezoneFinder
from pytz import timezone 

DEFAULT_TERM = 1480042675
DEFAULT_LONGITUDE = -37.76
DEFAULT_LATITUDE = 122.41

def main():
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

def query_local(latitude, longitude, utcTime):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lng=longitude, lat=latitude)

    tz = timezone(timezone_name)
    value = datetime.datetime.fromtimestamp(utcTime)
    aware_datetime = pytz.utc.localize(value)
    aware_datetime_in_local = aware_datetime.astimezone(tz)

    print(aware_datetime_in_local)

if __name__ == '__main__':
    main()
