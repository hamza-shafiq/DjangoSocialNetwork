import datetime

from django.contrib.auth.models import User
from posts.models import Location, HolidayInformation
from utils.abstarct_api import AbstractAPI


def save_user_location(user_id):
    """
    Refreshes all stocks in `stock_ids`, a list of ids.
    """
    abstract_api = AbstractAPI()
    geo_location = abstract_api.get_geolocation_content()
    geo_location["user_id"] = user_id

    # Create User Location
    user = User.objects.filter(id=user_id).first()
    user_location = Location.create_user_location(geo_location)

    # Create Holiday Location
    current_date = str(datetime.datetime.now().date()).split("-")
    holiday_list = []
    geo_locations = abstract_api.get_holidays(country_code=geo_location["country_code"], date=current_date)

    for loc in geo_locations:
        holiday_list.append(HolidayInformation(user_id=user_id, event=loc["event"], week_day=loc["week_day"]))

    # bulk create holiday information
    HolidayInformation.objects.bulk_create(holiday_list)

    print("===================================")
    print("User Location Created Successfully!")
    print("User: {} - Location: {}, {}.".format(user.username, user_location.city, user_location.country))
    print("===================================")
