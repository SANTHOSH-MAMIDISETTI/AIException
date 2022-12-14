
import io
import warnings
import numpy as np
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from PIL import Image
from stability_sdk import client
from torchvision.transforms import GaussianBlur


class Stable_Diff():
    """
    Class responsable for generating and editing images, connecting to the Stable Diffusion api
    """
    def __init__(self, key) -> None:
        self.key = key #'sk-okwwhQZ05mESHdEmD5tzi1bxiH97fIL7wWwjcYFrwFDfpLxs'
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
        img = img.resize((512, 512))
        stability_api = self.api # Set up our connection to the API.

        answers = stability_api.generate(prompt, sampler=generation.SAMPLER_K_DPMPP_2M )
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn("Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(str(artifact.seed)+ ".png") 
                    print("Image saved as " + str(artifact.seed) + ".png")

                    return img


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
                    img3.save(str(artifact.seed)+ "-5-completed.png") 

                    return img3

starting_img = Image.open('empty_room.jpg')
starting_img = starting_img.resize((512, 512))
gen_image = Stable_Diff().edit_image(starting_img, 'add an office chair next to the plant on the left, style is trendy')







