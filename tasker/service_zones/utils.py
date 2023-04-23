from shapely.geometry import Polygon, Point
from fire_alarm_objects.models import FireAlarmObject 
   
   
def add_fire_alarm_zone(service_zone):
    fire_alarm_objects = FireAlarmObject.objects.select_related('address').filter(branch = service_zone.branch)
    polygon_zone = Polygon(eval(service_zone.geopoints))
    for fire_alarm_object in fire_alarm_objects:
        geopoint = Point(eval(fire_alarm_object.address.get_geopoint()))
        if polygon_zone.contains(geopoint):
            fire_alarm_object.service_zone = service_zone
            fire_alarm_object.save()