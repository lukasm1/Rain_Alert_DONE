# twilio pw:

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient  # if u want to use pyanywhere, u need to hav this line

# and os.environ which hides sensitive data like pw, api id etc

# https://twiliodoer.secure.force.com/SenderId if Czech rep, then i need to set up this and charges 6 usd per m.


API_KEY = os.environ.get("OWM_API_KEY")  # Environment variable was first created in terminal and then this line

LAT = 41.327545
LON = 19.818699
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "ACf5418303292dfbd89af16fbbe74a633a"
auth_token = os.environ.get("OWM_API_TOKEN")  # same here, orig> a16eda7674aae40b3df8cc7e3d25a653

parameters = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
}

response = requests.get(url=API_ENDPOINT, params=parameters)
response.raise_for_status()
print(response)

data = response.json()["hourly"]
print(data)

twelve_h_list = data[:12]
print(twelve_h_list)

id_list = [twelve_h_list[_]["weather"][0]["id"] for _ in range(len(twelve_h_list))]
print(id_list)


def check_rain():
    for _ in range(12):
        if data[_]["weather"][0]["id"] <= 700:
            return True


def send_sms():
    if check_rain():
        proxy_client = TwilioHttpClient()  # and add this LINE
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}  # and this line
        client = Client(account_sid, auth_token, http_client=proxy_client)
        message = client.messages \
            .create(
            body="It's gonna rain today. Remember to bring an ☂️",
            from_='+15869913247',
            to='+420777537252',
        )
        print(message.status)


send_sms()