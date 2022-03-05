import datetime
from posts.models import Location, HolidayInformation
from utils.abstarct_api import AbstractAPI


def save_user_location(user_id):
    """
    Refreshes all stocks in `stock_ids`, a list of ids.
    """
    abstract_api = AbstractAPI()
    geo_location = abstract_api.get_geolocation_content()
    if geo_location:
        geo_location["user_id"] = user_id
        # Save User Location
        user_location = Location.create_user_location(geo_location)

        if user_location:
            # Save Holiday Information
            current_date = str(datetime.datetime.now().date()).split("-")
            holidays_info = abstract_api.get_holidays(country_code=geo_location["country_code"], date=current_date)

            if holidays_info:
                holiday_list = []
                for holiday in holidays_info:
                    holiday_list.append(HolidayInformation(
                        user_id=user_id,
                        event=holiday["event"],
                        week_day=holiday["week_day"])
                    )

                # bulk create holiday information
                HolidayInformation.objects.bulk_create(holiday_list)

    print("===================================")
    print("User Location Created Successfully!")
    print("===================================")
