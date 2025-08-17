#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import asyncio
import aiomysql
import json
import functools
import uuid
from  logs.log_config import logger


# Load the env variables
load_dotenv()



def get_filepath():
    """This is a function that returns a file path"""
    # Do not change the filename and folder_path
    filename = 'hospital_data.json'
    folder_path = './data'
    file_path = os.path.join(folder_path, filename)

    return file_path


async def db_connect():
    try:
        conn = await aiomysql.connect(
                    host=os.getenv('HOST'),
                    user=os.getenv('DB_USER'), 
                    password=os.getenv('PASSWORD'),
                    port=int(os.getenv('PORT')),
                    db=os.getenv('DATABASE_NAME')
                    )
        return conn
    except Exception as e:
        logger.error(f"An error occurred while connecting to db: {e}")
    


def data_insert_transactional(func):
    """This is decorator function to handle db_insert transaction"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        conn = args[0]
        cur = await conn.cursor()        
        async for data_yield in func(*args, **kwargs):
            # Generate the unique uuid for the hospital_id
            hospital_id = uuid.uuid4()
            try:
                await cur.execute("SELECT * FROM hospitals WHERE name = %s", (data_yield['name'],))
                result = await cur.fetchone()
                if result:
                    logger.info(f"❌hospital data already exists skipp")
                    continue
                else:
                    # convert the support_levels to accept string data
                    support_levels = ",".join(data_yield['support_levels'])
        
                    await cur.execute("""INSERT INTO hospitals(hospital_id, name, address, state, city, area, geo_lon, geo_lat, support_levels, phone)
                                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(hospital_id, data_yield['name'],
                                                                                      data_yield['address'],data_yield['state'], 
                                                                                      data_yield['city'], data_yield['area'], 
                                                                                      data_yield['longitude'], data_yield['latitude'],
                                                                                    support_levels, data_yield['phone'])
                                                                                    )
                    
                    await conn.commit()
                    
                    # print("data inserted successfully..")
                    logger.info(f"✅ Data inserted successfully..")
            except aiomysql.Error as e:
                logger.error(f"❌An error occurred while inserting data:{e}")
                logger.error(f"❌Rolling back db transaction...")
                await conn.rollback()

        # Close cursor after all the data has been inserted
        if cur:
            await cur.close()
            logger.info(f" Cursor closed successfully!")

    return wrapper



# # Call the function to return the filepath
file_path = get_filepath()

@data_insert_transactional
async def data_processing(conn, file_path):
    # This is a generator function to process data from the json file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for hos_data in data:
        yield hos_data



async def main():
    conn = await db_connect()
    try:
        await data_processing(conn, file_path=file_path)
    # close the connection after all the 
    finally:
        if conn:
            conn.close()
            print("connection closed")
            logger.info(f"✅ Connection to the database closed successfully!")





if __name__ == '__main__':
    # Runs the main coroutine for this program file
    asyncio.run(main())

