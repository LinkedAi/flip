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
import pkg.transforms as ts
import pkg.labeler as lr
import pkg.common as cm
import pkg.saver as sr
import numpy as np
import random
import uuid
import cv2
import os
import re

from pypeln import process as pr
from datetime import datetime
from glob import glob
from tqdm import tqdm

# ==============================================================================
# Environment global variables
# ==============================================================================
# Number of output images when the data_generator.py is ejecuted
N_SAMPLES = 10

# Data - path for background images
BACKGROUNDS_PATTERN = "data/backgrounds/*"

# Data - path for objects images
# TODO Create class selection
OBJECTS_PATTERN = "data/objects/**/*"

# current now date to create the result folder name for output images
DATE = datetime.now().strftime("%Y%m%d_%H%M%S")

# create name for result folder dir
OUT_DIR = "data/result/{}".format(DATE)

# Object randomization
# number of objects for full image
# (1) = only one image -
# (1,3) = random objects number
N_OBJECTS = (1, 5)
# ==============================================================================
# Functions
# ==============================================================================
def saveData():
    """
  Args:
  Description:
  Returns:
  """
    # make output dir
    os.makedirs(OUT_DIR, exist_ok=True)


def setupEnvirment(objects_pattern, backgrounds_pattern, n_samples):
    """
  Args:
    objects_pattern:      path for objects images
    backgrounds_pattern:  path for background images
    n_samples:            Number of output images when the data_generator.py 
                          is ejecuted
  Description:
  Returns: TODO
  """
    # 'glob' function finds all pathnames matching a specified pattern
    # get object paths
    objects_paths = glob(objects_pattern)
    # get background paths
    backgrounds_paths = glob(backgrounds_pattern)

    elements = []

    for _ in range(n_samples):
        el = createElement(objects_paths, backgrounds_paths)
        elements.append(el)

    # createGoogleCSV(elements)


def createElement(objects_paths, backgrounds_paths):
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
    objects = [createChild(i) for i in object_idxs]

    # get random background
    background_idx = np.random.randint(len(backgrounds_paths))
    background_image = cm.utils.inv_chanels(
        cv2.imread(backgrounds_paths[background_idx], cv2.IMREAD_UNCHANGED,)
    )

    # create new element
    el = ts.Element(background_image, objects)

    # Transformer element
    transformObjects = [
        ts.daug.RotateElement(ts.const.Rotation.random, min=-30, max=30),
        ts.daug.FlipElement(ts.const.Flip.y),
        # ts.RandomResize(mode=ts.const.Resize.symmetricw, wmin=160, wmax=200, hmin=160, hmax=200)
    ]

    name = uuid.uuid4()
    transform = ts.Compose(
        [
            ts.ApplyToObjects(transformObjects),
            # ts.daug.RotateElement(ts.const.Rotation.ninety),
            ts.ObjectsRandomResize(
                mode=ts.const.Resize.symmetricw, wmin=0.25, wmax=0.4, hmin=0.1, hmax=0.4
            ),
            ts.ObjectsRandomPosition(
                xmin=0, ymin=0.4, xmax=0.7, ymax=0.7, mode=ts.const.Position.percentage
            ),
            # ts.daug.FlipElement(ts.const.Flip.x),
            ts.ObjectsGetBGColor(),
            lr.CreateTags(),
            ts.DrawElement(),
            # lr.CreateTags(),
            sr.SaveImage(OUT_DIR, name),
            # sr.csv.CreateCSV(OUT_DIR, name)
            sr.json.CreateJson(OUT_DIR, name),
        ]
    )

    el = transform(el)

    return el


def createChild(path):
    img = cm.utils.inv_chanels(cv2.imread(path, cv2.IMREAD_UNCHANGED))

    split_name_temp = re.split(r"/|\\", path)
    split_name = split_name_temp[2]

    obj = ts.Element(img, name=split_name)

    return obj


def createGoogleCSV(elements):
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

            csv_data += f"{'TRAIN' if count <= train else ('VALIDATE' if count <= train + validate else 'TEST')},PATH#{element.name},{tag['name']}.jpg,{round(x1, 2)},{round(y1, 2)},,,{round(x2, 2)},{round(y2, 2)},,\n"
    # print(csv_data)

    with open("data/google_data.csv", mode="w") as f:
        f.write(csv_data)


# ==============================================================================
saveData()
setupEnvirment(OBJECTS_PATTERN, BACKGROUNDS_PATTERN, N_SAMPLES)

# stage = pr.map(create_element, range(N_SAMPLES), workers=WORKERS, on_start=on_start)
# stage = (x for x in tqdm(stage, total=N_SAMPLES))

# pr.run(stage)
