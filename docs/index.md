# Flip

<p align="left">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.7|%203.8-brightgreen.svg" alt="Python supported"></a>
</p>

Synthetic Data generation with Flip! Generate thousands of new 2D images from a small batch of objects and backgrounds.

## Installation

Install Flip using pip:

```bash
pip install flip-data
```

### Dependencies

Flip requires:
- Python (>= 3.7)
- Opencv (>= 4.3.0)
- Numpy (>= 1.19.1)

## Quick Start ([Example](https://github.com/linkedai/flip/blob/master/examples/README.md))

To try Flip library you can run ```examples/data_generator.py```. 
You will need to add background images and objects to compose your new training dataset, then
place them in the following directories:
```python
BACKGROUNDS_PATTERN = "examples/data/backgrounds/*"
OBJECTS_PATTERN = "examples/data/objects/**/*"
```

The main workflow in Flip is to create transformers and then execute them as follows: 

```python
## Import Flip transformers
import flip.transformers as tr

OUT_DIR = "examples/result"

...

## Create Child transformers
transform_objects = [
        tr.data_augmentation.Rotate(mode='random'),
        tr.data_augmentation.Flip(mode='y'),
        tr.data_augmentation.RandomResize(
            mode='symmetric_w',
            relation='parent',
            w_percentage_min=0.2,
            w_percentage_max=0.5
        )
    ]

## Create main transformer
transform = tr.Compose([
    tr.ApplyToObjects(transform_objects),
    tr.domain_randomization.ObjectsRandomPosition(
        x_min=0, y_min=0.4, x_max=0.7, y_max=0.7, mode='percentage'
    ),
    tr.data_augmentation.Flip('x'),
    tr.domain_randomization.Draw(),
    tr.labeler.CreateBoundingBoxes(),
    tr.io.CreateJson(out_dir=OUT_DIR, name='img_generate.jpg'),
    tr.io.CreateJson(out_dir=OUT_DIR, name='json_generated.jpg')
])

## Execute transformations
el = tr.Element(image=..., objects=...)
[el] = transform(el)
```

![Object](https://github.com/linkedai/flip/blob/master/docs/images/generated.jpg)

## Transformers 

The main transformers are:

- Transformer
- Compose
- ApplyToObjects

By the way, all Transformers will be executed over objects of class Element and will return a new _transformed_ Element.

### Data Augmentation

- Flip: Flip the Element in x or y axis.
- RandomResize: Change the size of an Element randomly.
- Rotate: Rotate Element randomly.

### Random Domain

- Draw: Draw objects over background Element to merge them into a new image.
- ObjectsRandomPosition: Set Random positions to objects over background Element.

### Labeler

- CreateBoundingBoxes: Draw bounding boxes around the objects contained by a background Element.

### IO

- SaveImage: Save a .jpg File with the new generated image.
- Json: Save generated Labels as a Json.
- Csv: Save generated Labels as a CSV.


## Want to Contribute or have any doubts or feedback?

If you want extra info, email me at flip@linkedai.co

## Report Issues

Please help us by [reporting any issues](https://github.com/linkedai/flip/issues/new/choose) you may have while using Flip.

## License

* [Flip License](https://github.com/linkedai/flip/blob/master/LICENSE)
