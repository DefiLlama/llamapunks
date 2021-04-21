import itertools
import random
import os
from PIL import Image


output_individual_sprites = True
shuffle = True
spritesheet_max_columns = 10

features = [
    'eyes',
    'head',
    'mouth'
]


def list_image_files(path: str):
    """ Return list file names of all image files in a folder """
    files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            try:
                Image.open(filepath).close()
            except Image.UnidentifiedImageError:
                continue
            else:
                files.append(filepath)
    return files

def ListToString(list):
    string = ""
    for element in list:
        string += "-" + element

    return string


random.seed(0)

feature_files = {
    'base': list_image_files(os.path.join('images', 'base'))
}
for feature in features:
    path = os.path.join('images', feature)
    feature_files[feature] = [None] + list_image_files(path)

if output_individual_sprites and not os.path.exists('sprites'):
    os.mkdir('sprites')

with Image.open(feature_files['base'][0]) as image:
    image_size = image.size

database = open('database.txt', 'w')
database.write('#number,base,attributes..\n')

combinations = list(itertools.product(*feature_files.values()))
total = len(combinations)
if shuffle:
    random.shuffle(combinations)

cols = min(total, spritesheet_max_columns)
rows = (total // spritesheet_max_columns) + 1
width = cols * image_size[0]
height = rows * image_size[1]
spritesheet = Image.new('RGBA', (width, height))

x = 0
y = 0

for (number, files) in enumerate(combinations):
    print(f'Generating llama {number+1}/{total}', end='\r')

    llama_image = Image.new('RGBA', image_size, )
    data = []

    for file in files:
        if file is None:
            continue

        with Image.open(file) as feature_image:
            llama_image.alpha_composite(feature_image)

        attributes = os.path.basename(file).split('.')[0]
        data.append(attributes)

    spritesheet.paste(llama_image, (x, y))
    x += image_size[0]
    if x >= spritesheet.width:
        x = 0
        y += image_size[1]

    if output_individual_sprites:
        llama_image = llama_image.resize((llama_image.width * 10, llama_image.height * 10), 0)
        llama_image.save(os.path.join('sprites', f'llama{ListToString(data)}.png'))

    database.write(','.join(data) + '\n')

spritesheet = spritesheet.resize((spritesheet.width * 10, spritesheet.height * 10), 0)
spritesheet.save('llamapunks.png')

database.close()