#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import asyncio
import aiomysql
import uuid


# load the env variables
load_dotenv()


class AsyncDbContext:
    """This is is a class that will handle the db creation and table"""
    def __init__(self):
        self.conn = None
        self.cur = None    

    async def __aenter__(self):
        try:
            self.conn = await aiomysql.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'), 
                password=os.getenv('PASSWORD'),
                port=int(os.getenv('PORT'))
                )
            self.cur = await self.conn.cursor()

            # Create the database
            await self.cur.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE_NAME')}")

            # connect/set the database to be used
            await self.cur.execute(f"USE {os.getenv('DATABASE_NAME')}")

            print(f"🗄️ Database created successfully")

        except aiomysql.Error as e:
            print(f"❌ An error occurred: {e}")
        
        # Return the cursor
        return self.cur
        
    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        # Close the connection if any unexccepted error
        if self.cur:
            await self.cur.close()
        if self.conn:
            self.conn.close()


# create the function that will create the table
async def async_create_table(cur):
    """This is a coroutine to create the user table"""
    try:
        await cur.execute("""CREATE TABLE IF NOT EXISTS hospitals (
                        hospital_id CHAR(36) PRIMARY KEY,
                        name VARCHAR(250) NOT NULL,
                        address VARCHAR(250) NOT NULL,
                        state VARCHAR(200) NOT NULL,
                        city VARCHAR(200) NOT NULL,    
                        geo_lan DECIMAL(9, 6) NOT NULL,
                        geo_lat DECIMAL(9, 6) NOT NULL,
                        support_levels ENUM('low', 'medium', 'high', 'critical'),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX hos_name (name),
                        INDEX hos_addr(address)
                        )""")    
        print("✅ Table were successfully created!")
    except aiomysql.Error as e:
        print(f" ❌ An error occurred while creating table: {e}")



async def main_context_handler():
    """This is main corountine to handle the db context for both db and tablecreation """
    async with AsyncDbContext() as cur:
        # create the table 
        await async_create_table(cur)

       

# This will run the main coroutine
asyncio.run(main_context_handler())



        





