import os
#import backend
import random
import pandas as pd


rooms = ['living_room', 'kitchen', 'bedroom', 'study_room', 'office', 'dining_room']
styles = ['abstract']
print(os.getcwd())

def read_txt_to_list(path):
    print(os.getcwd())
    with open(  path) as f:
     lines = [line.rstrip('\n') for line in f]
    return lines


dict = dict()
dict['living_roomabstract'] =  [
    'Create a living room with abstract art on the walls.',
    'Design a living room with abstract patterned furniture.',
    'Generate an image of a living room with an abstract rug.',
    'Imagine a living room with abstract paintings on the walls and colorful furniture.',
    'Visualize a living room with an abstract light fixture hanging from the ceiling.',
    'Create a living room with abstract sculptures on the coffee table and shelves.',
    'Generate an image of a living room with abstract wallpaper and modern furniture.',
    'Imagine a living room with abstract throw pillows and a cozy fireplace.',
    'Visualize a living room with an abstract chandelier and comfy armchairs.',
    'Create a living room with abstract wall art and a plush sofa.',
    'Generate an image of a living room with an abstract rug and a sleek coffee table.',
    'Imagine a living room with abstract paintings and a colorful ottoman.',
    'Visualize a living room with an abstract tapestry and a cozy reading nook.',
    'Create a living room with abstract sculptures and a statement bookshelf.',
    'Generate an image of a living room with abstract curtains and a trendy bar cart.',
    'Imagine a living room with abstract patterned throw pillows and a statement rug.',
    'Visualize a living room with abstract light fixtures and a plush sectional sofa.',
    'Create a living room with abstract paintings and a sleek dining table.',
    'Generate an image of a living room with abstract wallpaper and a comfortable armchair.',
    'Imagine a living room with abstract sculptures and a cozy fireplace.'
]

dict['kitchen_abstract'] = ['Create a kitchen with abstract art on the walls.', 'Design a kitchen with abstract patterned backsplash.', 'Generate an image of a kitchen with an abstract tile floor.', 'Imagine a kitchen with abstract paintings on the walls and colorful cabinets.', 'Visualize a kitchen with an abstract light fixture hanging from the ceiling.', 'Create a kitchen with abstract sculptures on the countertops and shelves.', 'Generate an image of a kitchen with abstract wallpaper and modern appliances.', 'Imagine a kitchen with abstract throw pillows and a cozy breakfast nook.', 'Visualize a kitchen with an abstract chandelier and comfy bar stools.', 'Create a kitchen with abstract wall art and a sleek island.', 'Generate an image of a kitchen with an abstract backsplash and a trendy range hood.', 'Imagine a kitchen with abstract paintings and a colorful backsplash.', 'Visualize a kitchen with an abstract tapestry and a cozy kitchen table.', 'Create a kitchen with abstract sculptures and a statement backsplash.', 'Generate an image of a kitchen with abstract curtains and a sleek refrigerator.', 'Imagine a kitchen with abstract patterned throw pillows and a statement bar stools.', 'Visualize a kitchen with abstract light fixtures and a plush kitchen island.', 'Create a kitchen with abstract paintings and a sleek sink.', 'Generate an image of a kitchen with abstract wallpaper and a comfortable countertop.', 'Imagine a kitchen with abstract sculptures and a cozy fireplace.']

dict['bedroom_abstract'] = ['Create a bedroom with abstract art on the walls.', 'Design a bedroom with abstract patterned bedding.', 'Generate an image of a bedroom with an abstract rug.', 'Imagine a bedroom with abstract paintings on the walls and colorful furniture.', 'Visualize a bedroom with an abstract light fixture hanging from the ceiling.', 'Create a bedroom with abstract sculptures on the nightstands and shelves.', 'Generate an image of a bedroom with abstract wallpaper and modern furniture.', 'Imagine a bedroom with abstract throw pillows and a cozy reading nook.', 'Visualize a bedroom with an abstract chandelier and comfy armchairs.', 'Create a bedroom with abstract wall art and a plush bed.', 'Generate an image of a bedroom with an abstract rug and a sleek dresser.', 'Imagine a bedroom with abstract paintings and a colorful ottoman.', 'Visualize a bedroom with an abstract tapestry and a cozy seating area.', 'Create a bedroom with abstract sculptures and a statement bookshelf.', 'Generate an image of a bedroom with abstract curtains and a trendy vanity.', 'Imagine a bedroom with abstract patterned throw pillows and a statement rug.', 'Visualize a bedroom with abstract light fixtures and a plush armchair.', 'Create a bedroom with abstract paintings and a sleek desk.', 'Generate an image of a bedroom with abstract wallpaper and a comfortable rocking chair.', 'Imagine a bedroom with abstract sculptures and a cozy fireplace.']

dict['study_room_abstract'] = ['A colorful abstract study room with geometric-shaped furniture.', 'A minimalist abstract study room with sleek, modern furniture.', 'A dreamy abstract study room with floating furniture and pastel hues.', 'A futuristic abstract study room with transparent furniture and neon lights.', 'A playful abstract study room with furniture in various shapes and sizes.', 'An industrial abstract study room with metal furniture and exposed brick walls.', 'A tropical abstract study room with bright, vibrant furniture and palm leaves.', 'An elegant abstract study room with plush, velvet furniture and gold accents.', 'A cozy abstract study room with plush furniture and warm, earthy tones.', 'A whimsical abstract study room with furniture in unique, organic shapes.', 'A retro abstract study room with geometric furniture and bold, geometric patterns.', 'A romantic abstract study room with delicate, floral furniture and soft pastels.', 'An abstract study room with floating furniture and a water-like color scheme.', 'A futuristic abstract study room with transparent furniture and futuristic technology.', 'An abstract study room with furniture in the shape of animals and nature elements.', 'A rustic abstract study room with wooden furniture and warm, earthy tones.', 'An abstract study room with furniture in the shape of clouds and sky elements.', 'A modern abstract study room with clean, geometric furniture and bold colors.', 'An abstract study room with furniture in the shape of abstract art and sculptures.', 'A playful abstract study room with furniture in various colors and patterns.']
#print(dict['study_room_abstract'])


## If you have prompts seperated by ENTER: use
# dict['room_style'] = txt_to_list(path)


#make sure your room_style is in the dict!!!
def get_prompt(room, style):
    key = room+'_'+style
    list = dict[key]

    prompt = random.choice(list)
    return prompt

#prompt = get_prompt('kitchen', 'abstract')
#print(prompt)
#print(get_prompt('study_room', 'abstract'))


def link_prompt_to_furniture(labels, room, style):
    dataset = pd.read_csv('dataset.csv')
    #print(dataset)
    items = [] #label[0] is for item[0]
    
    for label in labels:
        print(label)
        this_item = dataset[dataset['label'].str.contains(label)]
        print(this_item)
        # if you wanna add style to the label in the future
        # this_style = this_item[style in dataset['label'.contains(label)]]
        item = this_item.sample() # obviously then change 'this_item' to 'this_style'
        items.append(item)
    return items
        
items = link_prompt_to_furniture(labels = ['chair', 'bed', 'sofa'], room = 'living', style='doesnt matter')
print(items[0]['link'])                        