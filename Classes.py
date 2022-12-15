from tempfile import TemporaryFile
import openai

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




##### FELIX



### TO-DO's:
# openai.error.InvalidRequestError: We could not parse the JSON body of your request. (HINT: This likely means you aren't using your HTTP library correctly. The OpenAI API expects a JSON payload, but what was sent was not valid JSON. If you have trouble figuring out how to fix this, please send an email to support@openai.com and include any relevant code you'd like help with.)
# Solve this error, find out got formatting to add the strings 


### Classes to build:
#  - Handlers to call the other API 
#  - Whisper (free API key should be available by lablab)
#  - Dall-E / Stable Diffusion (done)
#  - Codex (done)
#  - OCR 
#  - YOLO (image detection)

class GPT3_Convo():
    def __init__(self) -> None:
        self.model= "text-davinci-003",
        key_path = str("api_key.txt")
        openai.api_key_path=key_path

        #TO-DO: write a nice prompt to use GPT3 as assistant bot
        #'User:' in the end such that GPT3 would understand that user is talking to it
        self.conversation = """
        You are Exception, an AI assistant created by AI Exception. Please respond to this conversation:\n User: 
        """
        print('Convo model created')

    def update_conversation(self, new_prompt, response):
        # this keeps all the previous info to its input 
        # \n is the character for new line TO-DO: find out if this is useful for GPT3?
        self.conversation = self.conversation +  new_prompt + """
        Exception: """ + response + """
         User: """


    def prompt_conversation(self, new_prompt, temperature = 0.7, max_tokens= 1000):

        # add new prompt to existing conversation
        prompt = self.conversation + new_prompt 
        #print(type(prompt))

        response = openai.Completion.create(
        model=self.model,
        prompt= prompt,
        temperature= temperature, 
        max_tokens=max_tokens,
        # TO-DO: figure out if we would want to be able to change these parameters below? If so: add to function call
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        print(response)
        self.update_conversation(self, new_prompt, response)
        return response



class GPT3_Classifier:
    def __init__(self) -> None:
        self.model= "text-davinci-003"
        key_path = str("key.txt")
        openai.api_key_path=key_path


    def classify(self, prompt):
        prompt = """Classify the next sentence in of these 4 labels: [generate image], [factcheck], [write code], [write message]:
        """ + prompt #prompts - santosh 
        
        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=0, #?
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        output = str(response['choices'][0]).split('text": ')[1].replace(r'\n\n', '').replace(r'\n', '')

        return output


class GPT3_Prompt_Handler:

    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "text-davinci-003"

    def handle_prompt(self, prompt_action, prompt):
        prompt = """Rewrite the follow input as a """ + prompt_action + """ prompt:
        """ + prompt #prompts - santosh 
        
        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=0, 
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        
        output = str(response['choices'][0]).split('text": ')[1].replace(r'\n\n', '').replace(r'\n', '')
    
        return output


###### FRANCESCO


class Codex_Gen: 
    """
    Class responsable for generating code, connecting to the Codex api
    Input: prompt (programming language explicitly needed)
    """
    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "code-davinci-002"

    def codex_gen(self, prompt):

        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        return response

# class stable diffusion - santosh 
class Dall_E_Gen: 
    """
    Class responsable for generating images, connecting to the Dall-E2 api
    Input: prompt (the more detailed the better)
    """
    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path

    def image_gen(self, prompt):
        
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']

        return image_url



# class stable diffusion -santosh 
class Dall_E_Edit: 
    """
    Class responsable for editing pictures, connecting to the Dall-E2 api
    Input: 
        image_path = string containing the path of the whole image to edit
        masked_image_path = string containing the path of the image having a mask on 
        prompt = description of the full new image, not just the erased/masked area
        https://beta.openai.com/docs/guides/images/usage
    """
    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
    
    def image_edit(self, image_path, masked_image_path, prompt):
        
        response = openai.Image.create_edit(
        image=open(image_path, "rb"),
        mask=open(masked_image_path, "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']

        return image_url


class GPT3_Message_Gen: 
    """
    Class responsable for generating messages and emails, connecting to the GPT-3 api
    Input: prompt = input for writing the message
    """
    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "text-davinci-003"

    def message_gen(self, prompt):
        prompt = """Write a message using the information of the following prompt. prompt:
        """ + prompt
        
        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=0.3, 
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        
        output = str(response['choices'][0]).split('text": ')[1].replace(r'\n\n', '').replace(r'\n', '')
        
        return output



class Google_Search: 
    def __init__(self) -> None:
        pass
    def google_search(link):
        pass
"""question = "What are the Three (3) biggest countries, and their respective sizes?"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+")
}"""

class Whisper():
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


class Stable_Diff():
    """
    Class responsable for generating and editing images, connecting to the Stable Diffusion api
    Input: API KEY for stable diffusion 
    """
    def __init__(self, key= 'sk-okwwhQZ05mESHdEmD5tzi1bxiH97fIL7wWwjcYFrwFDfpLxs') -> None:
        self.key = key # API Key available 'sk-okwwhQZ05mESHdEmD5tzi1bxiH97fIL7wWwjcYFrwFDfpLxs'
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
        label, style, material = params
        temp_data = self.data[self.data['label'] == label]
        temp_data = temp_data[temp_data['style'] == style]
        temp_data = temp_data[temp_data['material'] == material]
        url = list(temp_data['url'])[0]

        return url




def text_to_speech(text, lang = 'en'):
    tts = gTTS(text, lang = lang)  
    tts.save('temp.mp3')
    playsound.playsound('temp.mp3')



def main():
    language = 'en'
    classifier = GPT3_Classifier()
    prompt_handler = GPT3_Prompt_Handler()
    
    #user_input = Whisper.rec(5)
    
    user_input = """Write a mail to my boss explaining I like his daughter"""
    
    action = classifier.classify(user_input)
    print(action) # classification output 
    

    if "Write Message" in action:
        message_gen = GPT3_Message_Gen()
        prompt_cleansed = prompt_handler.handle_prompt("""GPT3""", user_input,)
        message = message_gen.message_gen(prompt_cleansed)
        print('message')
        print(message)
        output_spoken = message
        

    elif "Write Code" in action:
        code_gen = Codex_Gen()
        prompt_cleansed = prompt_handler.handle_prompt("""Codex""", user_input,)
        code = code_gen.codex_gen(prompt_cleansed)
        print(code)


    elif "Generate Image" in action:
        im_gen = Dall_E_Gen()
        prompt_cleansed = prompt_handler.handle_prompt("""Dall_E""", user_input,)
        im_url = im_gen.image_gen(prompt_cleansed)
        print(im_url)

   
    if output_spoken:
        text_to_speech(output_spoken)
        



if __name__=='__main__':
    main()