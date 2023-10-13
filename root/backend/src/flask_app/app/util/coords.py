from math import pi,cos,sin,sqrt,pow,atan2

def distance_between_coords(lat1: float, lon1: float, lat2: float, lon2: float):
    """Returns the distance between two coordinates
    in meters. Coordinates are between -180° to 180°"""

    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (lon2 - lon1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    meters = 6367000 * c

    return meters