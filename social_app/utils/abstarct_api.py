import requests
from requests.adapters import HTTPAdapter, Retry
import json
from django.conf import settings


class AbstractAPI:
    def __init__(self):
        self.GEO_API_KEY = settings.GEO_API_KEY
        self.HD_API_KEY = settings.HD_API_KEY
        self.EV_API_KEY = settings.EV_API_KEY
        self.BASE_URL = "https://{}.abstractapi.com/v1/"

    def get_geolocation_content(self):
        url = self.BASE_URL.format("ipgeolocation")
        result_set = {}

        try:
            payload = "{}?api_key={}".format(url, self.GEO_API_KEY)

            # API hit retries if it fails due to server error
            s = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            response = s.get(payload)
            if response.status_code == 200:
                resp = json.loads(response.content)

                result_set = {
                    "ip_address": resp["ip_address"],
                    "city": resp["city"],
                    "region": resp["region"],
                    "country": resp["country"],
                    "country_code": resp["country_code"],
                    "postal_code": resp["postal_code"],
                    "latitude": resp["latitude"],
                    "longitude": resp["longitude"],
                }

        except Exception as e:
            print("Exception occur while calling abstract api to get user geo-location. Error: {}".format(str(e)))

        return result_set

    @staticmethod
    def extract_info(param):
        return {
            "event": param["name"],
            "week_day": param["week_day"],
        }

    def get_holidays(self, country_code, date):
        url = self.BASE_URL.format("holidays")
        holiday_info = []

        try:
            payload = "{}?api_key={}&country={}&year={}&month={}&day={}".format(
                url, self.HD_API_KEY, country_code, date[0], date[1], date[2])

            response = requests.get(payload)
            resp_list = json.loads(response.content)
            holiday_info = [self.extract_info(each_holiday) for each_holiday in resp_list]

        except Exception as e:
            print("Exception occur while calling abstract api to fetch holidays. Error: {}".format(str(e)))

        return holiday_info

    def validate_email(self, email):
        email_validity = {"is_valid_format": False}
        url = self.BASE_URL.format("emailvalidation")

        try:
            payload = "{}?api_key={}&email={}".format(url, self.EV_API_KEY, email)
            response = requests.get(payload)
            if response.status_code == 200:
                resp = json.loads(response.content)
                email_validity["deliverability"] = resp["deliverability"]
                email_validity["is_valid_format"] = resp["is_valid_format"]["value"]
                email_validity["is_smtp_valid"] = resp["is_smtp_valid"]["value"]

        except Exception as e:
            print("Exception occur while calling abstract api to validate email. Error: {}".format(str(e)))

        return email_validity
