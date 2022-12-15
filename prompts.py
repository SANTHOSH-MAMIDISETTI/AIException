import os
#import backend
import random


rooms = ['living_room', 'kitchen', 'bedroom', 'hallway', 'study_room', 'office', 'dining_room']
styles = ['abstract']
print(os.getcwd())

def read_txt_to_list(path):
    print(os.getcwd())
    with open('backend/' + path) as f:
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

## If you have prompts seperated by ENTER: use
# dict['room_style'] = txt_to_list(path)



def get_prompt(room, style):
    key = room+'_'+style
    list = dict[key]

    prompt = random.choice(list)
    return prompt

prompt = get_prompt('kitchen', 'abstract')
print(prompt)
