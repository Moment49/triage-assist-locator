#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import asyncio
import aiomysql
import json
import time
import functools

filename = '../data/hospital_data.json'


def data_insertion(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper



@data_insertion
def data_processing():
    # This is a generator function to process data from the json file
    pass



def hospital_data(filename):
    print("This is hospital data")
    with open(filename, 'r') as file:
        data = json.load(file)

    yield data

for data in hospital_data(filename):
    print(data)



