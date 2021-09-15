# Flip Documentation

## [Data Augmentation](https://github.com/LinkedAi/flip/tree/master/flip/transformers/data_augmentation)

### Brightness(value = float, force = boolean): 

Change the brightness of the element.

Arguments:
- Value: Change factor. -> {Float>0 where a number less than 1 decreases the brightness in percentage while a higher number increases it in percentage (1 default).}
- Force (optional): Force change in all elements. -> {True (default), False}

### Color(color = str, force = boolean): 

Change color space or the element color.

Arguments:
- Color: Color space code. -> {'hsv', 'lab', 'xyz', 'luv', 'gray' (default), 'red', 'green', 'blue', 'purple', 'yellow', 'cyan'}
- Force (optional): Force change in all elements. -> {True (default), False}

### Contrast(value = float, force = boolean): 

Change the contrast of the element.

Arguments:
- Value: Change factor. -> {Float>0 where a number less than 1 decreases the contrast in percentage while a higher number increases it in percentage (1 default).}
- Force (optional): Force change in all elements. -> {True (default), False}

### Saturation(value = float, force = boolean): 

Change the saturation of the element.

Arguments:
- Value: Change factor. -> {Float>0 where a number less than 1 decreases the saturation in percentage while a higher number increases it in percentage (1 default).}
- Force (optional): Force change in all elements. -> {True (default), False}

### CutOut(figure = str, color = str, mode = str, x_min = float, x_max = float, y_min = float, y_max = float, crop_shape = (int, int), num = int, force = boolean): 

Remove a section of the element in the desired area.

Arguments:
- Figure: The shape of the cut. -> {'rectangle' (default), 'circle', 'square', 'triangle'}
- Color: The color of the cut. -> {'red', 'green', 'blue', 'black' (default), 'white'} 
- Mode: If it is 'random' it cuts anywhere in the element. Otherwise, take the percentages given in the variables x_min, y_min, x_max and y_max. -> {'random' (default), 'percentage'}
- X_min (optional): The minimum percentage of the image where cutting begins in the image on the x-axis. -> {Float between 0 and 1}
- X_max (optional): The maximum percentage of the image where cutting begins in the image on the x-axis. -> {Float between 0 and 1}
- Y_min (optional): The minimum percentage of the image where cutting begins in the image on the y-axis. -> {Float between 0 and 1}
- Y_max (optional): The maximum percentage of the image where cutting begins in the image on the y-axis. -> {Float between 0 and 1}
- Crop_shape (optional): Cut size in x and y respectively. -> {Int between 0 and the width and length of the image respectively}
- Num (optional): Number of cuts. -> {Int > 0 (1 default)}
- Force (optional): Force change in all elements. -> {True (default), False}

### Flip(mode = str, force = boolean): 

Flip the element in x or y axis.

Arguments: 
- Mode: If it is 'random' flip the element on any of the axes. Otherwise, it rotates it about the selected axis. -> {'random', 'x', 'y'}
- Force (optional): Force change in all elements. -> {True (default), False}

### Noise(mode = str, value = float, force = boolean): 

Add noise to the element image.

Arguments: 
- Mode: Choose the type of noise to add to the element. -> {'gaussian_blur', 'avg_blur', 'median_blur', 'salt_pepper' (default)}
- Value: Percentage in which you want to modify the element, except in the avg_blur that does not need it. -> {Float between 0 and 1 (0.5 default)}
- Force (optional): Force change in all elements. -> {True (default), False}

### RandomCrop(x_min = float, y_min = float, force = boolean): 

Cut the image randomly.

Arguments: 
- X_min (optional): The minimum percentage of the image to cut on the x-axis. If no value is presented, a random one is assigned. -> {Float between 0 and 1}
- Y_min (optional): The minimum percentage of the image to cut on the y-axis. If no value is presented, a random one is assigned. -> {Float between 0 and 1}
- Force (optional): Force change in all elements. -> {True (default), False}

### RandomResize(mode = str, w_min = float, w_max = float, h_min = float, h_max = float, relation = str, w_percentage_min = float, w_percentage_max = float, h_percentage_min = float, h_percentage_max = float, force = boolean): 

Change the size of an Element randomly.

Arguments:
- Mode: If it is 'symmetric_h' it changes the size with respect to the y-axis of the element, if it is 'symmetric_w' it changes the size with respect to the x-axis of the element, otherwise it changes each of the dimensions separately. -> {'asymmetric' (default), 'symmetric_w', 'symmetric_h'}
- W_min: The minimum size of the image to make the change with respect to the x-axis. -> {Int > 0}
- W_max: The maximun size of the image to make the change with respect to the x-axis. -> {Int > 0}
- H_min: The minimum size of the image to make the change with respect to the y-axis. -> {Int > 0}
- H_max: The maximun size of the image to make the change with respect to the y-axis. -> {Int > 0}
- Parent: If it is 'parent', the percentages are expected to calculate the change with respect to the size of the element. Otherwise, the quantities specified in x_min, x_max, y_min and y_max are taken. -> {'none' (default), 'parent'}
- W_percentage_min (optional): The minimum percentage of the image to make the change with respect to the x-axis. -> {Float between 0 and 1}
- W_percentage_max (optional): The maximun percentage of the image to make the change with respect to the x-axis. -> {Float between 0 and 1}
- H_percentage_min (optional): The minimum percentage of the image to make the change with respect to the y-axis. -> {Float between 0 and 1}
- H_percentage_max (optional): The maximun percentage of the image to make the change with respect to the y-axis. -> {Float between 0 and 1}
- Force (optional): Force change in all elements. -> {True (default), False}

### Rotate(mode = str, min = float, max = float, force = boolean): 

Rotate Element randomly.

Arguments:
- Mode: If it is 'random' it rotates the element within the determined angles, if it is '90' it rotates the element in 90 degree angles and if it is 'upside_down' it rotates the element in 180 degree angles. -> {'random' (default), '90', 'upside_down'}
- Min: The minimum angle to rotate the element. -> {Int between 0 and 360 (0 default)}
- Max: The maximum angle to rotate the element. -> {Int between 0 and 360 (360 default)}
- Force (optional): Force change in all elements. -> {True (default), False}

## [Domain Randomization](https://github.com/LinkedAi/flip/tree/master/flip/transformers/domain_randomization)

### Draw( ):

Draw objects over background Element to merge them into a new image.

It has no parameters.

### ObjectsRandomPosition(mode = str, x_min = float, x_max = float, y_min = float, y_max = float, force_overlap = boolean):

Set Random positions to objects over background Element.

Arguments:
- Mode: If it is 'percentage' it takes the corresponding percentages to take the origin of the element. Otherwise it takes the corresponding values to take the origin of the element. -> {'none' (default), 'percentage'}
- X_min (optional): Percentage or minimum value on the x-axis to position the object. -> {Float between 0 and 1 or Float > 0. (0% default)}
- X_max (optional): Percentage or minimum value on the x-axis to position the object. -> {Float between 0 and 1 or Float > 0. (100% default)}
- Y_min (optional): Percentage or minimum value on the y-axis to position the object. -> {Float between 0 and 1 or Float > 0. (0% default)}
- Y_max (optional): Percentage or minimum value on the y-axis to position the object. -> {Float between 0 and 1 or Float > 0. (100% default)}
- Force_overlap (optional): If true, it allows overlapping between elements in the image, otherwise, it does not allow elements to touch each other. -> {True (default), False}

## [IO](https://github.com/LinkedAi/flip/tree/master/flip/transformers/io)

### CreateCSV(out_dir = str name = str):

Save generated Labels as a CSV.

Arguments:
- Out_dir: Path where you want to save the file.
- Name: Name with which you want to save the file.

### CreateJson(out_dir = str name = str):

Save generated Labels as a Json.

Arguments:
- Out_dir: Path where you want to save the file.
- Name: Name with which you want to save the file.

### CreatePascalVoc(out_dir = str name = str):

Save generated Labels as a XML.

Arguments:
- Out_dir: Path where you want to save the file.
- Name: Name with which you want to save the file.

### SaveImage(out_dir = str name = str):

Save a .jpg File with the new generated image.

Arguments:
- Out_dir: Path where you want to save the image.
- Name: Name with which you want to save the image.

### SaveMask(out_dir = str name = str):

Save a .jpg File with the new generated mask.

Arguments:
- Out_dir: Path where you want to save the mask.
- Name: Name with which you want to save the mask.

## [Labeler](https://github.com/LinkedAi/flip/tree/master/flip/transformers/labeler)

### CreateBoundingBoxes( ):

Draw bounding boxes around the objects contained by a background Element.

It has no arguments.

### CreateMasks( ):

Creates the segmentation mask for the objects contained in a background element.

It has no arguments.

## [Transformer](https://github.com/LinkedAi/flip/blob/master/flip/transformers):

### ApplyToBackground(Transformer):

It allows to carry out the different changes and transformations in sequence only to the background element.

Inside it, the transformations are placed in the order that you want to be carried out, as shown in the [example](https://github.com/linkedai/flip/blob/master/examples/README.md).

### ApplyToCreatedImage(Transformer):

It allows to carry out the different changes and transformations in sequence only to the created image element.

Inside it, the transformations are placed in the order that you want to be carried out, as shown in the [example](https://github.com/linkedai/flip/blob/master/examples/README.md).

### ApplyToObjects(Transformer):

It allows to carry out the different changes and transformations in sequence only to the objects elements.

Inside it, the transformations are placed in the order that you want to be carried out, as shown in the [example](https://github.com/linkedai/flip/blob/master/examples/README.md).

### Compose(Transformer):

Allows to carry out the different changes and transformations in sequence to the elements.

Inside it, the transformations list are placed in the order that you want to be carried out, as shown in the [example](https://github.com/linkedai/flip/blob/master/examples/README.md).

### Element( ):

The Element class represents the base class than can be use by a Transform.

Commonly used arguments are:
- image: Numpy Array with the image of the element.
- name: A name for the element can be use for label it.
- objects: Child Elements of this element, mostly used when the parent Element is a background.

Commonly extra arguments:
- x, y: To set the position of the element over a parent element.
- tags: To save the information of the generated tags for the child objects.