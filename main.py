import requests as re
from math import sin, cos, sqrt, atan2, radians
import datetime
import os

IP1 = '87.97.95.255'
IP2 = '188.143.34.195'
EARTH_RADIUS = 6371


class GetGeolocation:
    def __init__(self, apikey, ip):
        self.apikey = apikey
        self.ip = ip

    def run(self):
        start_time = datetime.datetime.now()
        response = re.get('https://api.ipinfodb.com/v3/ip-city/?key={}&ip={}&format=json'.format(self.apikey, self.ip))
        end_time = datetime.datetime.now()
        self.response_time = (end_time - start_time).total_seconds()
        response = response.json()
        self.statusCode = response['statusCode']
        self.statusMessage = response['statusMessage']
        self.ipAddress = response['ipAddress']
        self.countryCode = response['countryCode']
        self.countryName = response['countryName']
        self.regionName = response['regionName']
        self.cityName = response['cityName']
        self.zipCode = response['zipCode']
        self.latitude = float(response['latitude'])
        self.longitude = float(response['longitude'])
        self.timeZone = response['timeZone']


def distance(start_latitude, start_longitude, end_latitude, end_longitude):
    start_latitude = radians(start_latitude)
    start_longitude = radians(start_longitude)
    end_latitude = radians(end_latitude)
    end_longitude = radians(end_longitude)

    dlat = end_latitude - start_latitude
    dlon = end_longitude - start_longitude

    a = sin(dlat / 2) ** 2 + cos(start_latitude) * cos(end_latitude) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(EARTH_RADIUS * c)


def calc_speed(dist, time):
    if dist > 0 and time > 0:
        return str(round(dist / time)) + ' km/h'
    elif dist == 0:
        return 0
    elif time == 0:
        return 'Teleporting'


def calc_validation(dist, time):
    if time > 0:
        speed = dist / time
        if dist < 50:
            THRESHOLD = 150
        elif 50 <= dist < 200:
            THRESHOLD = 300
        elif dist >= 200:
            THRESHOLD = 700
    if time == 0:
        return '\033[1;31m' + 'Incredible' + '\033[0m'
    elif speed > THRESHOLD:
        return '\033[1;31m' + 'Incredible (threshold: ' + str(THRESHOLD) + ')\033[0m'
    else:
        return '\033[0;32m' + 'Valid (threshold: ' + str(THRESHOLD) + ')\033[0m'


def date_format_check(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y.%m.%d %H:%M:%S')
        return True
    except ValueError:
        return False


def change_API_key(new=False):
    cls()
    api_key = input(' New ipinfodb.com API key: ')
    new_api_file = open("api_key.txt", "w")
    new_api_file.write(api_key)
    new_api_file.close()
    if not new:
        main_menu()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def intro():
    cls()
    print('')
    print(' *************************')
    print(' *       GEOLOCATOR      *')
    print(' *************************')
    print('  powered by ipinfodb.com')
    print('')


def main_menu(intro=False):
    if not intro:
        cls()
    print(' [0] Get IP info')
    print(' [1] Get distance')
    print(' [2] Get speed')
    print(' [3] Change API key')
    print(' [4] Exit')
    decision = input(' --> ')
    if decision == '0':
        getIPinfo_menu()
    elif decision == '1':
        getDistance_menu()
    elif decision == '2':
        get_speed_menu()
    elif decision == '3':
        change_API_key()
    elif decision == '4':
        pass
    else:
        print(' Choose from the following options: 1, 2, 3')
        main_menu()


def getIPinfo_menu():
    cls()
    print(' * Get IP info *')
    ip = input(' IP address: ')
    ip_check = GetGeolocation(API_KEY, ip)
    print(' API request in progress from https://api.ipinfodb.com')
    ip_check.run()
    print(' \033[93m' + ip_check.statusMessage + '\033[0m')
    print(' Response time:', ip_check.response_time, 's')
    print(' *********************')
    print(' IP address:', ip_check.ipAddress)
    print(' Country:   ', ip_check.countryName)
    print(' Region:    ', ip_check.regionName)
    print(' City:      ', ip_check.cityName)
    print(' Latitude   ', ip_check.latitude)
    print(' Longitude  ', ip_check.longitude)
    print(' Time zone: ', ip_check.timeZone)
    print(' *********************')
    input()
    main_menu()


def getDistance_menu():
    cls()
    print(' * Get distance *')
    ip1 = input(' First IP address: ')
    ip2 = input(' Second IP address: ')
    ip_check1 = GetGeolocation(API_KEY, ip1)
    ip_check2 = GetGeolocation(API_KEY, ip2)
    print(' API request in progress from https://api.ipinfodb.com')
    ip_check1.run()
    ip_check2.run()
    print(' \033[93m' + ip_check1.statusMessage + '\033[0m')
    dist = distance(ip_check1.latitude, ip_check1.longitude, ip_check2.latitude, ip_check2.longitude)
    print(' *********************')
    print(' From:', ip_check1.countryName + ',', ip_check1.cityName)
    print(' To:', ip_check2.countryName + ',', ip_check2.cityName)
    print(' Distance:', dist, 'km')
    print(' *********************')
    input()
    main_menu()


def get_speed_menu():
    cls()
    print(' * Get speed *')
    ip1 = input(' First IP address: ')
    ip2 = input(' Second IP address: ')
    while True:
        while True:
            time1 = input(' First time: ')
            if date_format_check(time1):
                time1 = datetime.datetime.strptime(time1, '%Y.%m.%d %H:%M:%S')
                break
            else:
                print(' Wrong time format! (yyyy.mm.dd hh:mm:ss)')
        while True:
            time2 = input(' Second time: ')
            if date_format_check(time2):
                time2 = datetime.datetime.strptime(time2, '%Y.%m.%d %H:%M:%S')
                break
            else:
                print(' Wrong time format! (yyyy.mm.dd hh:mm:ss)')
        if (time2 - time1).total_seconds() >= 0:
            break
        else:
            print('The second time cannot be earlier than the first time!')
    time = ((time2 - time1).total_seconds() / 60 / 60)
    ip_check1 = GetGeolocation(API_KEY, ip1)
    ip_check2 = GetGeolocation(API_KEY, ip2)
    print(' API request in progress from https://api.ipinfodb.com')
    ip_check1.run()
    ip_check2.run()
    print(' \033[93m' + ip_check1.statusMessage + '\033[0m')
    dist = distance(ip_check1.latitude, ip_check1.longitude, ip_check2.latitude, ip_check2.longitude)
    speed = calc_speed(dist, time)
    print(' *********************')
    print(' From:', ip_check1.countryName + ',', ip_check1.cityName)
    print(' To:', ip_check2.countryName + ',', ip_check2.cityName)
    print(' Distance:', dist, 'km')
    print(' Speed: ', speed)
    print(' ' + calc_validation(dist, time))
    print(' *********************')
    input()
    main_menu()


if __name__ == '__main__':

    try:
        api_file = open('api_key.txt', 'r')
        API_KEY = api_file.read()
        api_file.close()
    except FileNotFoundError:
        change_API_key(True)
        api_file = open('api_key.txt', 'r')
        API_KEY = api_file.read()
        api_file.close()

    intro()
    main_menu(True)
