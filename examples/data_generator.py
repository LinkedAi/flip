# ==============================================================================
"""
Code Information:
	Developers:  Diego Parra     - LinkedAi  - diego@linkedai.co
              Juan Jurado(JJ) - LinkedAi  - jj@linkedai.co
Description:
  - TODO: Some description about this .py file
Tested on:
    python 3.7.5
    OpenCV 4.1.2
    Ubuntu 19.10
"""
# ==============================================================================
# Import useful packages
# ==============================================================================
import flip
import numpy as np
import random
import uuid
import cv2
import os
import re

# from pypeln import process as pr
from datetime import datetime
from glob import glob
# from tqdm import tqdm

# ==============================================================================
# Environment global variables
# ==============================================================================
# Number of output images when the data_generator.py is ejecuted
N_SAMPLES = 200

# Data - path for background images
BACKGROUNDS_PATTERN = "examples/data/backgrounds/*"

# Data - path for objects images
# TODO: Create class selection
OBJECTS_PATTERN = "examples/data/objects/**/*"

# current now date to create the result folder name for output images
DATE = datetime.now().strftime("%Y%m%d_%H%M%S")

# create name for result folder dir
OUT_DIR = "examples/result/{}".format(DATE)

# Object randomization
# number of objects for full image
# (1) = only one image -
# (1,3) = random objects number
N_OBJECTS = (1, 5)


# ==============================================================================
# Functions
# ==============================================================================
def create_out_dir():
    """
  Args:
  Description:
    Create an empty folder with the name define in the OUT_DIR var to save the generated data.
  Returns: null
  """
    # make output dir
    os.makedirs(OUT_DIR, exist_ok=True)


def setup_environment(objects_pattern, backgrounds_pattern, n_samples):
    """
  Args:
    objects_pattern:      path for objects images
    backgrounds_pattern:  path for background images
    n_samples:            Number of output images when the data_generator.py 
                          is ejecuted
  Description:
  Returns: TODO
  """
    # 'glob' function finds all path_names matching a specified pattern
    # get object paths
    objects_paths = glob(objects_pattern)
    # get background paths
    backgrounds_paths = glob(backgrounds_pattern)

    elements = []

    for _ in range(n_samples):
        el = create_element(objects_paths, backgrounds_paths)
        elements.append(el)

    create_google_csv(elements)


def create_element(objects_paths, backgrounds_paths):
    """
  Args:
  Description:
  Returns:
  """
    # Check if N_OBJECTS is iterable and define amount of objects
    if hasattr(N_OBJECTS, "__iter__"):
        n_objs = np.random.randint(low=N_OBJECTS[0], high=N_OBJECTS[1] + 1)
    else:
        n_objs = N_OBJECTS

    # get random elements
    object_idxs = np.random.choice(objects_paths, n_objs)

    # Create elements for the object images
    objects = [create_child(i) for i in object_idxs]

    # get random background
    background_idx = np.random.randint(len(backgrounds_paths))
    background_image = flip.utils.inv_channels(
        cv2.imread(backgrounds_paths[background_idx], cv2.IMREAD_UNCHANGED,)
    )

    # create new element
    el = flip.transformers.Element(image=background_image, objects=objects)

    # Transformer element
    transform_objects = [
        flip.transformers.data_augmentation.Rotate(mode='random'),
        flip.transformers.data_augmentation.Flip(mode='y'),
        flip.transformers.data_augmentation.RandomResize(
            mode='symmetric_w',
            relation='parent',
            w_percentage_min=0.2,
            w_percentage_max=0.5
        )
    ]

    name = uuid.uuid4()
    transform = flip.transformers.Compose(
        [
            flip.transformers.ApplyToObjects(transform_objects),
            # ts.daug.RotateElement(ts.const.Rotation.ninety),
            # flip.transformers.data_augmentation.ObjectsRandomResize(
            #     mode='symmetric_w', w_min=0.25, w_max=0.4, h_min=0.1, h_max=0.4
            # ), TODO: Modify to work with Apply to Objects
            flip.transformers.domain_randomization.ObjectsRandomPosition(
                x_min=0, y_min=0.4, x_max=0.7, y_max=0.7, mode='percentage'
            ),
            flip.transformers.data_augmentation.Flip('x'),
            # ts.ObjectsGetBGColor(), TODO: Modify to work with Apply to Objects
            flip.transformers.domain_randomization.Draw(),
            flip.transformers.labeler.CreateBoundingBoxes(),
            flip.transformers.io.SaveImage(OUT_DIR, name),
            # flip.transformers.io.CreateCSV(OUT_DIR, name)
            flip.transformers.io.CreateJson(OUT_DIR, name),
        ]
    )

    [el] = transform(el)

    return el


def create_child(path):
    img = flip.utils.inv_channels(cv2.imread(path, cv2.IMREAD_UNCHANGED))

    split_name_temp = re.split(r"/|\\", path)
    index = len(split_name_temp) - 2
    split_name = split_name_temp[index] if index >= 0 else split_name_temp[0]

    obj = flip.transformers.Element(image=img, name=split_name)

    return obj


def create_google_csv(elements):
    csv_data = ""

    count = 0
    train = len(elements) * 0.8
    validate = len(elements) * 0.2

    for element in elements:
        count += 1

        bh = element.image.shape[0]
        bw = element.image.shape[1]

        for tag in element.tags:
            x1 = tag["pos"]["x"] / bw
            y1 = tag["pos"]["y"] / bh
            x2 = (tag["pos"]["x"] + tag["pos"]["w"]) / bw
            y2 = (tag["pos"]["y"] + tag["pos"]["h"]) / bh

            if x1 > 1:
                x1 = 1
            if y1 > 1:
                y1 = 1
            if x2 > 1:
                x2 = 1
            if y2 > 1:
                y2 = 1

            csv_data += f"{'TRAIN' if count <= train else ('VALIDATE' if count <= train + validate else 'TEST')},PATH#{element.name}.jpg,{tag['name']},{round(x1, 2)},{round(y1, 2)},,,{round(x2, 2)},{round(y2, 2)},,\n"
    # print(csv_data)

    with open("examples/result/google_data.csv", mode="w") as f:
        f.write(csv_data)


# ==============================================================================
create_out_dir()
setup_environment(OBJECTS_PATTERN, BACKGROUNDS_PATTERN, N_SAMPLES)

# stage = pr.map(create_element, range(N_SAMPLES), workers=WORKERS, on_start=on_start)
# stage = (x for x in tqdm(stage, total=N_SAMPLES))

# pr.run(stage)
