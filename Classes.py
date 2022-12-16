from tempfile import TemporaryFile
import openai
import random
import requests
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
from io import BytesIO
import playsound
import io
import warnings
import numpy as np
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
from stability_sdk import client
from torchvision.transforms import GaussianBlur



class Whisper():  # FOR FUTURE IMPLEMENTATIONS 
    """
    Class responsable for generating messages and emails, connecting to the GPT-3 api
    Input: prompt = input for writing the message
    """
    def __init__(self) -> None:
        pass 

    def rec(num_seconds): # Duration of recording
        fs = 44100  # Sample rate 
        myrecording = sd.rec(int(num_seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        write('sound.wav', fs, myrecording)  

        url = "https://whisper.lablab.ai/asr"
        payload={}
        files=[
        ('audio_file',('sound.wav',open('sound.wav','rb'),'audio/mpeg'))
        ]
        response = requests.request("POST", url, data=payload, files=files).json()
        output = response['text']

        return output


def text_to_speech(text, lang = 'en'):
    tts = gTTS(text, lang = lang)  
    tts.save('temp.mp3')
    playsound.playsound('temp.mp3')


class Stable_Diff():
    """
    Class responsable for generating and editing images, connecting to the Stable Diffusion api
    Input: API KEY for stable diffusion 
    """
    def __init__(self, key= 'sk-w3uG3THRYH92M23HYfrR848QRfPJdpYru8RT8fzsfU38d7dw') -> None:
        self.key = key 
        self.host = 'grpc.stability.ai:443'
        self.api = client.StabilityInference(
            key=self.key, # API Key reference.
            verbose=True, # Print debug messages.
            engine="stable-diffusion-v1-5", # Set the engine to use for generation. For SD 2.0 use "stable-diffusion-v2-0".
            # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 
            # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
            )

    def txt_to_image(self, prompt):
        """
        Input: prompt to generate an image
        """
        #img = img.resize((512, 512))
        stability_api = self.api # Set up our connection to the API.

        answers = stability_api.generate(prompt, sampler=generation.SAMPLER_K_DPMPP_2M )
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn("Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    filename = str(artifact.seed)+ ".png"
                    img.save(filename) 
                    print("Image saved as " + filename)

                    return img, filename


    def edit_image(self, img, prompt):
        """
        Inputs: 
        img = image to be edited, in a .png or a .jpg format 
        prompt = prompt for changing the image, adding furniture
        """
        img = img.resize((512, 512))
        stability_api = self.api # Set up our connection to the API.

        answers2 = stability_api.generate(prompt,init_image=img,start_schedule=0.6,seed=54321,steps=30,cfg_scale=7.0,width=512,height=512,sampler=generation.SAMPLER_K_DPMPP_2M)
        for resp in answers2:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn("Your request activated the API's safety filters and could not be processed.""Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    global img2
                    img2 = Image.open(io.BytesIO(artifact.binary))
                    img2.save(str(artifact.seed)+ "-2-img2img.png") 
        img2_grayscale = img2.convert('L')
        img2_a = np.array(img2_grayscale)
        mask = np.array(img2_grayscale)
        mask[img2_a<150] = 0  
        mask[img2_a>=150] = 1 
        strength = .2  
        d = int(255 * (1-strength))
        mask *= 255-d 
        mask += d
        mask = Image.fromarray(mask)
        mask.save(str(artifact.seed)+ "-3-mask.png") 
        blur = GaussianBlur(11,20)
        mask = blur(mask)
        mask.save(str(artifact.seed)+ "-4-featheredmask.png")
        answers3 = stability_api.generate(prompt,init_image=img2,mask_image=mask,start_schedule=1,seed=1823948,steps=30,cfg_scale=8.0,width=512,height=512,sampler=generation.SAMPLER_K_DPMPP_2M)
        for resp in answers3:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    global img3
                    img3 = Image.open(io.BytesIO(artifact.binary))
                    filename = str(artifact.seed)+ "-5-completed.png"
                    img3.save(filename) 
                    print("Image saved as " + filename)

                    return img3, filename




class Dataset_Handler:
    """
    Class responsable for extracting the url of the wanted item, connecting to our internal database.
    Inputs:
        __init__: dataset = pandas_dataset type database of our furniture
        find_url: params = list containing [label, style, material] wanted 
    """
    def __init__(self, dataset) -> None:
        self.data = dataset 

    def find_url(self, params): 
        label, style, room = params
        temp_data = self.data[self.data['label'] == label]
        temp_data = temp_data[temp_data['style'] == style]
        temp_data = temp_data[temp_data['room'] == room]
        temp_url = list(temp_data['url'])
        url = random.choice(temp_url)

        return url


class Prompt_Gen():
    def __init__(self) -> None:
        pass

    def presets(self, style, room):
        inp = 'Add several furniture items such as tables, chairs or beds to this '+str(room)+' using a '+str(style)+' style'
        print(inp)
        return inp 








