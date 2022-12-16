import Classes
from botocore.config import Config
import logging
import boto3
from botocore.exceptions import ClientError
import os
import YOLO.detect as yolo
import glob
from PIL import Image
from flask import Flask, request
import flask
import json
from io import BytesIO
from flask_cors import CORS
import requests 
import re
import random
import pandas as pd 
import json
import streamlit as st


def main():

    
    FE_BE = {
    'prompt':'',
    'style':'modern',
    'room':'bedroom',
    'url':'',
    } #from front end 

    #unpack from FE
    #input_pic = Image.open(BytesIO(requests.get(received_data['url']))) #TODOO!! FRANCESCO
    input_pic = Image.open('empty_test.png') 
    FE_prompt = FE_BE['prompt']
    style = FE_BE['style']
    room = FE_BE['room']

    img_generator = Classes.Stable_Diff()
    if FE_prompt == '': # edit image 

        prompt_editing = Classes.Prompt_Gen().presets(style, room)
        pic, filename = img_generator.edit_image(input_pic, prompt_editing)
        # GENERATE URL FOR PIC AND SEND IT TO S3 BUCKET, ADD IT TO THE FINAL JSON

        pred, image, img_file = yolo.run(source = filename)
        final_data = []
        custom_db = pd.read_csv('custom_db.csv')

        for item in pred:
            temp_label = item['label']
            if 'table' in temp_label:
                temp_label = 'table'
                print('table present')

            if 'bed' in temp_label:
                temp_label = 'bed'
                print('bed present')

            temp_params = [temp_label, style, room]
            try:
                temp_url = Classes.Dataset_Handler(custom_db).find_url(temp_params)
                item['url'] = temp_url
                final_data.append(item)
            except:
                continue

        print(final_data)
        BE_FE = json.dumps(final_data, indent=2)
        # BE_FE IS THE FINAL JSON TO SEND TO FRONT END 



    elif FE_prompt != '': # create image 
        pic, filename = img_generator.txt_to_image(FE_prompt)
        return pic 
        # GENERATE URL FOR PIC AND SEND IT TO S3 BUCKET, SEND IT TO FRONT END 
    
    st.title('Ultimate Furniture')
    st.write('project blahblah')

    st.header('Playground Area')
    st.write('Here is the playground...')

    st.image(pic)




    st.caption('The team member names ')



if __name__ == '__main__':
    main()
    #app.run("localhost", 6969)