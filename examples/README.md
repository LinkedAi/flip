# Flip: Examples

In this section you can find some examples to try the Flip library. 

## Install

Install Flip using pip:

```bash
pip install flip-data
```

## Examples

For this example we are going to use some open source datasets,
one for the objects that are going to be [butterflies](http://www.josiahwang.com/dataset/leedsbutterfly/) and
other for the backgrounds that have some [forest textures](http://textures.forrest.cz/).

#### Object:
![Butterfly](http://www.josiahwang.com/dataset/leedsbutterfly/examples/001.jpg)

#### Background:
![Three](http://textures.forrest.cz/textures/library/2009_forest/IMG_0303.jpg)

### crop_image_from_mask.ipynb

The first step to make this example work is gather the objects as segmented images.

1. Download [butterflies](http://www.josiahwang.com/dataset/leedsbutterfly/examples/001.jpg)
and unzip in a folder call `raw_data/` inside `examples/`.
2. Run all the blocks of the `crop_image_from_mask.ipynb` notebook.
3. Check all images were created and are in the folder `examples/data/objects/` divide in 10 categories.
4. Download [some textures](http://textures.forrest.cz/) and place them in `examples/data/backgrounds/`.

![Object](https://github.com/linkedai/flip/blob/master/docs/images/object.png)

### data_generator.py

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
        tr.data_augmentation.Color(color='red'),
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
        x_min=0, y_min=0.4, x_max=0.7, y_max=0.7, mode='percentage', force_overlap=False
    ),
    tr.data_augmentation.Flip('x'),
    tr.domain_randomization.Draw(),
    tr.labeler.CreateBoundingBoxes(),
    tr.labeler.CreateMasks(classes_names),
    tr.io.SaveImage(OUT_DIR, name),
    tr.io.SaveMask(OUT_DIR, name),
    tr.io.CreateJson(out_dir=OUT_DIR, name='img_generate.jpg'),
    tr.io.CreateJson(out_dir=OUT_DIR, name='json_generated.jpg')
])

## Execute transformations
el = tr.Element(image=..., objects=...)
[el] = transform(el)
```

To try the `data_generator.py` run:

```batch
python3 examples/data_generator.py
```

![Object](https://github.com/linkedai/flip/blob/master/docs/images/generated.png)

And their respective mask:

![Object](https://github.com/linkedai/flip/blob/master/docs/images/generatedM.png)

### show_labels.ipynb

With this notebook you can check your labels by changing the `PATH` to the name of the folder created in results.

![Object](https://github.com/linkedai/flip/blob/master/docs/images/generatedBB.png)

## Datasets

### [Butterflies](http://www.josiahwang.com/dataset/leedsbutterfly/)

Josiah Wang, Katja Markert, and Mark Everingham,
Learning Models for Object Recognition from Natural Language Descriptions,
In Proceedings of the 20th British Machine Vision Conference (BMVC-2009).

### [Forest](http://textures.forrest.cz/)

Texture library, Maintained by Michal Franc.