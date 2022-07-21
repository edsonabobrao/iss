import requests
import datetime as dt

SMTP_ADDR = 'smtp.gmail.com'
SENDER = 'sevandijapatel@gmail.com'
SDR_PASS = 'qphctdorzdsqcmbn'

MY_LATITUDE = 43.573150
# MY_LATITUDE = -50
# MY_LONGITUDE = 164
MY_LONGITUDE = -79.743250
response = requests.get(url='http://api.open-notify.org/iss-now.json')
response.raise_for_status()
data = response.json()

latitude = float(data['iss_position']['latitude'])
longitude = float(data['iss_position']['longitude'])
#
# iss_position = (longitude, latitude)
# print(iss_position)
parameters = {
    'lat': MY_LATITUDE,
    'lng': MY_LONGITUDE,
    'formatted': 0
}


def is_iss_up():
    return abs(latitude - MY_LATITUDE) < 5 and abs(longitude - MY_LONGITUDE) < 5


def is_dark():
    return (sunset < time_now.hour < 24) or time_now.hour < sunrise


response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

# print(sunrise)
# print(sunset)
# print(latitude)
# print(longitude)
print(abs(latitude - MY_LATITUDE))
print(abs(longitude - MY_LONGITUDE))

time_now = dt.datetime.now()

# print(time_now.hour)

## If ISS is close and is currently dark then email to tell me to look up
if is_dark() and is_iss_up():
    import smtplib

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=SENDER, password=SDR_PASS)
            connection.sendmail(
                from_addr=SENDER,
                to_addrs='fdpsaraiva@gmail.com',
                msg=f'Subject:ISS\n\nLook up! The ISS is out there!'
            )
    except ConnectionError:
        print('Couldn\'t connect to the SMTP server')
