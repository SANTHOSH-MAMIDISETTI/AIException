import openai

### TO-DO's:
# openai.error.InvalidRequestError: We could not parse the JSON body of your request. (HINT: This likely means you aren't using your HTTP library correctly. The OpenAI API expects a JSON payload, but what was sent was not valid JSON. If you have trouble figuring out how to fix this, please send an email to support@openai.com and include any relevant code you'd like help with.)
# Solve this error, find out got formatting to add the strings 


### Classes to build:
# 
class GPT3_Convo():

    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "text-davinci-003",


        # TO-DO: write a nice prompt to use GPT3 as assistant bot
        self.conversation = """You are Exception, an AI assistant created by AI Exception. Please respond to this conversation:\n
        User: """
        # 'User:' in the end such that GPT3 would understand that user is talking to it

        print('Convo model created')


    def prompt_conversation(self, new_prompt, temperature = 0.7, max_tokens= 1000):

        # add new prompt to existing conversation
        prompt = self.conversation + new_prompt 
        print(prompt)
        print(type(prompt))

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

        self.update_conversation(self, new_prompt, response)

        return response

    def update_conversation(self, new_prompt, response):
        

        # \n is the character for new line TO-DO: find out if this is useful for GPT3?
        self.conversation = self.conversation +  new_prompt + """
        Exception: """ + response + """
         User: """


class GPT3_Classifier:

    def __init__(self):
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "text-davinci-003"

    

    def classify(self, prompt):

        prompt = """Classify the next sentence in of these 4 labels: [generate image], [factcheck],  [translate], [write code]:
        """ + prompt
        

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
        print(output)

        return output


class GPT3_Prompt_Handler:

    def __init__(self) -> None:
        key_path = str("key.txt")
        openai.api_key_path=key_path
        self.model= "text-davinci-003"

    def handle_prompt(self, prompt, prompt_action):
        prompt = """Rewrite the follow input as a """ + prompt_action + """ prompt:
        """ + prompt
        print(prompt)
        

        response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=0, 
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        print(response)
        output = str(response['choices'][0]).split('text": ')[1].replace(r'\n\n', '').replace(r'\n', '')
        print(output)

        return output

prompt_handler = GPT3_Prompt_Handler()
prompt_cleaned = prompt_handler.handle_prompt("""Write the code used for making the fibonnacci sequence""", """Codex""")
print(prompt_cleaned)
# classifier = GPT3_Classifier()
# action = classifier.classify("""Generate pic of Obama writing code""")



# convo_bot = GPT3_Convo()
# # This crashes because of some string parsing error, I assume
# convo_bot.prompt_conversation("""Hey Exception, how are you? """)