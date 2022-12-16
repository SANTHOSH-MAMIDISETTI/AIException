import streamlit as st
from PIL import Image
import io
import Classes
import YOLO.detect as yolo
import pandas as pd 



header = st.container()
app = st.container()
playground = st.container()
img_generator = Classes.Stable_Diff()

with header:
    st.title('Ultimate Designs')
    st.write('An OpenAI powered tool that helps users generate interior designs effortlessly.') 
    st.write('Redesign your room in different styles, Easy and Free!') 
    st.write('Here are some examples:')

    col1, col2, col3 = st.columns(3)

    show1 = Image.open('show1.png') 
    show2 = Image.open('show2.png')
    show3 = Image.open('show3.png') 
    show3 = show3.resize((512, 512))

    col1.image(show1)
    col2.image(show2)
    col3.image(show3)





with app:

    st.header('Reimagine Room')
    st.write('Select your desired prompts and uplaod a picture of your room')


    style = st.selectbox('Which style: ', options=['Modern','Colorful'])
    room = st.selectbox('Which room is it: ', options=['Living Room', 'Bedroom', 'Study Room'])
    in_pic = st.file_uploader('Upload your picture here')

    if in_pic is not None:
        bytes_data = in_pic.getvalue()
        stream = io.BytesIO(bytes_data)
        img = Image.open(stream)

        prompt_editing = Classes.Prompt_Gen().presets(style, room)
        st.write(prompt_editing)
        pic, filename = img_generator.edit_image(img, prompt_editing)
        st.image(pic)

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

            if 'chair' in temp_label:
                temp_label = 'chair'
                print('chair present')

            if 'couch' in temp_label:
                temp_label = 'couch'
                print('couch present')

            temp_params = [temp_label, style, room]

            try:
                temp_url = Classes.Dataset_Handler(custom_db).find_url(temp_params)
                print(temp_url)
                item['url'] = temp_url
                st.write('Link to buy the '+str(item['label'])+ ' seen in the generated picture:')
                st.write(str(item['url']))
            except:
                continue


with playground:

    st.header('Stable Diffusion Playground')
    st.write('Imagination is your only limit! Go wild!')

    in_prompt = st.text_input('Prompt: ', '')

    if in_prompt != '':
        pic, filename = img_generator.txt_to_image(in_prompt)
        st.image(pic)
        



        






st.caption('The team member names ')
