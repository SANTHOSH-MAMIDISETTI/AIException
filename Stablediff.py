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

def text_to_img_stable_diffusion(prompt):

    answers = stability_api.generate(prompt,seed=992446758,steps=30, cfg_scale=8.0, width=512,height=512,samples=1,sampler=generation.SAMPLER_K_DPMPP_2M )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(str(artifact.seed)+ ".png") 
                print("Image saved as " + str(artifact.seed) + ".png")

prompt = input("Enter the text you want to generate an image for: ")
text_to_img_stable_diffusion(prompt)


# def editing_previous_img(img):