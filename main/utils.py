#!/usr/bin/env python3
from dotenv import load_dotenv
import asyncio
import aiomysql
import functools
from config.utils import db_connect
from logs.log_config import logger
from geopy.geocoders import Nominatim
from math import cos, sqrt, radians, asin, sin


load_dotenv()

# Note: Assume the standard Average speed in Nigera - 60KM
AVG_SPEED = 60

# Assume mean radius of earth (Haversin standard)
R = 6371


def log_user_interaction(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        username = kwargs['username']
        user_location = kwargs['user_location']
        user_severity = kwargs['user_severity']
        logger.info(f"User:{username}, location:{user_location}, severity:{user_severity}")
       
        # For async generators, do not await, just return the generator object
        results = func(*args, **kwargs)
        async for data in results:
            yield data
    return wrapper


def cal_hospital_eta(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        user_location = kwargs['user_location']
        # For async generators, do not await, just return the generator object
        results = func(*args, **kwargs)
        geolocator = Nominatim(user_agent="triage-location-service")
        logger.info(f"This is the geolocator object that will be \
                    returned once whic will be used to get the lat and lon coordinates: {geolocator}")
        location =  geolocator.geocode(f"{user_location}")
        victim_lat = location.latitude
        victim_lon = location.longitude
        cordinates = (victim_lon, victim_lat)

        logger.info(f"User current location cordinates: {cordinates}")

        # Reyielding the results
        async for data in results:
            for dat in data:
                hosp_lon = dat['geo_lon']
                hosp_lat = dat['geo_lat']

                # Calculate the haversine distance
                # Assume mean radius of earth (Haversin standard)
                global R
                # convert the lat and lon to radians for both hospital and victim location
                hosp_lat1 = radians(hosp_lat)
                hosp_lon1 = radians(hosp_lon)
                victim_lat2 = radians(victim_lat)
                victim_lon2 = radians(victim_lat)

                #Radian distance between each location 
                dLat = radians(victim_lat2 - hosp_lat1)
                dLon = radians(victim_lon2 - hosp_lon1)

                # Haversine Formular to calculate the distance
                a = sin(dLat/2)**2 + cos(hosp_lat1)*cos(victim_lat2)*sin(dLon/2)**2
                c = 2*asin(sqrt(a))

                # Cacluate the Overall distance in KM between the two points round off to 2 decimals
                distance = round(R * c, 2)

               
                # Now caculate the ETA (Expected time of arrival)
                # We use the simple formular (Note: since distance is in KM 
                # will convert the time to minutues by multiplying by 60)
                # Calculate EAT using formular, time = distance / average speed 
                # Plan to use and api or use geo data to get varying average speeds based on certain locations
                global AVG_SPEED

                # Round off the EAT to one decimal place
                ETA = round((distance / AVG_SPEED) * 60, 2)

                # Append the ETA and distance to the yielded data
                dat['ETA_in_minutes'] = ETA
                dat['distance'] = distance
                logger.info(f"final research result info for the user on hospital arrival: ETA -{ETA} minutes, distance in KM-{distance} to {dat['name']} facilty")
            yield data
    return wrapper



@log_user_interaction
@cal_hospital_eta
async def get_hosp_severity(username, user_location, user_severity):
    conn =  await db_connect()
    cur = await conn.cursor(aiomysql.DictCursor)
    await cur.execute("SELECT * FROM hospitals WHERE support_levels LIKE %s ", (user_severity))
    results = await cur.fetchall()
    yield results



# This coroutine is used to test any changes to be made to the above async generators/decorators
# async def main_coroutine():
#     results = get_hosp_severity(username='Elvis', user_location='Lagos', user_severity='High')
#     async for data in results:
#         print(data)



# if __name__ == '__main__':
#     asyncio.run(main_coroutine())