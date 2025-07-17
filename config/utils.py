#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import asyncio
import aiomysql
import json
import time


path = os.getcwd()

filename = '../data/hospital_data.json'
# print(filename)





def hospital_data(filename):
    print("This is hospital data")
    with open(filename, 'r') as file:
        data = json.load(file)

    yield data

for data in hospital_data(filename):
    print(data)
