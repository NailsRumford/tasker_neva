from dadata import Dadata
from tasker.settings import DADATA_SECRET, DADATA_TOKEN
from fire_alarm_objects.models import Address
from datetime import datetime

def clean_address(address):
    dadata = Dadata(token=DADATA_TOKEN, secret=DADATA_SECRET)
    result = dadata.clean("address", address)
    verification_status = result['qc']
    if verification_status != 0:
        raise Exception()
    address = result['result']
    latitude = result['geo_lat']
    longitude = result['geo_lon']
    address_object, status = Address.objects.get_or_create(
        address=address,
        latitude=latitude,
        longitude=longitude)
    return address_object

def clean_date (date_string):
    day, month, year = date_string.split(".")
    year = "20" + year
    new_date_string = datetime.strptime(f"{year}-{month}-{day}",'%Y-%m-%d')
    return new_date_string