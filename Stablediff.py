import os
import io
import warnings
import numpy as np
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from PIL import Image
from stability_sdk import client
from torchvision.transforms import GaussianBlur

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = 'sk-okwwhQZ05mESHdEmD5tzi1bxiH97fIL7wWwjcYFrwFDfpLxs'
stability_api = client.StabilityInference(key=os.environ['STABILITY_KEY'], verbose=True, engine="stable-diffusion-v1-5", )


# prompt = input("Enter the text you want to generate an image for: ")
# text_to_img_stable_diffusion(prompt)
# editing_previous_img(new_prompt)

def text_to_img_stable_diffusion(prompt):
    # answers = stability_api.generate(prompt,seed=992446758,steps=30, cfg_scale=8.0, width=512,height=512,samples=1,sampler=generation.SAMPLER_K_DPMPP_2M )
    answers = stability_api.generate(prompt,sampler=generation.SAMPLER_K_DPMPP_2M )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.""Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(str(artifact.seed)+ ".png") 
                print("Image saved as " + str(artifact.seed) + ".png")
                print("this is func 1")
    return img
# new_prompt = input("Enter the text you want to edit the previous image for: ")

def editing_previous_img (img,new_prompt):
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
    answers3 = stability_api.generate(new_prompt,init_image=img2,mask_image=mask,start_schedule=1,seed=1823948,steps=30,cfg_scale=8.0,width=512,height=512,sampler=generation.SAMPLER_K_DPMPP_2M)
    for resp in answers3:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img3
                img3 = Image.open(io.BytesIO(artifact.binary))
                img3.save(str(artifact.seed)+ "-5-completed.png") 
                print("this is func 2")


prompt = input("Enter the text you want to generate an image for: ")
imgs = text_to_img_stable_diffusion(prompt)
new_prompt = input("Enter the text you want to edit the previous image for: ")
# editing_previous_img("img.png",new_prompt)
editing_previous_img(imgs,new_prompt)