import csv
import argparse
import datetime
from geopy.geocoders import Nominatim

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
        query_by_cood(input_values.lat, input_values.lon, input_values.utc)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

def query_by_cood(latitude, longitude, utc):
    geolocator = Nominatim()
    location = geolocator.reverse("{}, {}".format(latitude, longitude))
    print(location.address)
    myzip = location.raw['address']['postcode']

    zipcodes = {}
    with open('zipcode.csv', newline='') as csvfile:
        zipreader = csv.reader(csvfile)
        flag = False
        for row in zipreader:
            ''' skip the header row '''
            if flag is False:
                flag = True
                continue
            offset = int(row[5])
            zipcodes[row[0]] = offset

    offset = zipcodes[myzip]
    print("offset: ", offset)

    value = datetime.datetime.fromtimestamp(utc)
    print("UTC: ", value)

    hour_diff = datetime.timedelta(hours=offset)
    print("local time: ", value + hour_diff)

if __name__ == '__main__':
    main()
