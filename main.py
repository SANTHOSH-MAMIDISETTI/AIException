import Classes
from botocore.config import Config
import logging
import boto3
from botocore.exceptions import ClientError
import os
import YOLO.detect as yolo
import glob
from PIL import Image



my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
client = boto3.client('kinesis', config=my_config)
s3 = boto3.client('s3')

def upload_file(file_name,  object_name=None, bucket = "exception"):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    # WAIT FOR API
    # GET PROMPT ( + INPUT PICTURE) + UNIQUE ID
    img_generator = Classes.Stable_Diff()

    unique_id = '0000'


    input_pic = None
    #input_pic = Image.open('example.png')
    prompt = 'A uni cafeteria with metal tables and chairs'

    if input_pic:
        
        pic, filename = img_generator.edit_image(input_pic, prompt)

    else:
        pic, filename = img_generator.txt_to_image(prompt)
    
    upload_file(filename, object_name= unique_id+'generated.jpg')
    

    ### WAIT FOR API:
    edit = None
    # This should also be in a while loop perhaps? so you can keep on editing?
    if edit:
        prompt = prompt # Get new prompt from API
        edit_pic, filename = img_generator.edit_image(pic, prompt)

        # Now we are overwriting filename to make it work with YOLO
        
        

    else:
        pred, image, img_file = yolo.run(source = filename)

        # Get the files that have the boxes saved
        glob_path_boxes = img_file.split('exa')[0]+'crops/**/*.json'
        print(glob_path_boxes)
        path_boxes = glob.glob(glob_path_boxes)

        # Upload all boxes
        for file in path_boxes:
            #make filename less complicated:
            fn = file.split('detect/')[-1]
            with open(file, 'rb') as f:
                
                s3.upload_fileobj(f, "exception", fn)
        
        ### TODO DatasetHandler




if __name__ == '__main__':
    
    main()