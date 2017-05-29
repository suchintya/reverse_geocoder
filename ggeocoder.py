import googlemaps
import csv

def main():
    print("hello geocoder")
    gmaps = googlemaps.Client(key='AIzaSyBwWbpO0rWqF711QzMDoMU2YcFjBK9gUvA')
    with open('Adresses_TN2.csv') as csvin:
        with open('latlng2.csv','w',newline='') as csvout:
            spamwriter = csv.writer(csvout)
            batchreader = csv.reader(csvin)
            for row in batchreader:
                address = row[1]+" "+row[2]+" "+row[3]
                print(address)
                geocode_result = gmaps.geocode(address)
                if(len(geocode_result) > 0):
                    lat = geocode_result[0]['geometry']['location']['lat']
                    lng = geocode_result[0]['geometry']['location']['lng']
                    print(str(lat)+" "+str(lng))
                    write_row=list(row)
                    write_row.append(lat)
                    write_row.append(lng)
                    write_row.append(encode(lat,lng,8))
                    spamwriter.writerow(write_row)

__base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
__decodemap = { }
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i
del i

def encode(latitude, longitude, precision=12):

    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    geohash = []
    bits = [ 16, 8, 4, 2, 1 ]
    bit = 0
    ch = 0
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even

        if bit < 4:
            bit += 1
        else:
            geohash += __base32[ch]
            bit = 0
            ch = 0

    return ''.join(geohash)

if __name__ == '__main__':
    main()
