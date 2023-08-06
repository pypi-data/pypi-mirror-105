# GGB Color Space

This package is implementation of GGB color space from [Development of a Robust Algorithm for Detection of Nuclei and Classification of White Blood Cells in Peripheral Blood Smear Image](https://link.springer.com/content/pdf/10.1007%2Fs10916-018-0962-1.pdf).


## Installation

This package could be installed via [PyPI](https://pypi.org/project/ggb/).

    pip3 install ggb


## Quick Demo

This package supports various computer vision libraries such as OpenCV and PIL. Complete example for these computer vision libraries provided in [here](https://github.com/reshalfahsi/ggb/tree/master/examples). For the short example in Python3:


```python
# import the package and its necessary components
from ggb import GGB, ColorSpace

# we are using OpenCV
import cv2

import urllib.request as urllib
import numpy as np

# load image from internet
req = urllib.urlopen('https://github.com/reshalfahsi/GGB/raw/master/docs/img/leukocytes.png')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)
    
# convert to GGB Color
ggb_image = GGB(image=img, input_color=ColorSpace.BGR).process()

# show the result    
ggb_image.show()

# save the image to OpenCV format
img = ggb_image.write()
```


## Result

### Leukocytes
![alt text](https://github.com/reshalfahsi/GGB/raw/master/docs/img/GGB_RGB_LEUKOCYTES.jpg)

### Fundus
![alt text](https://github.com/reshalfahsi/GGB/raw/master/docs/img/GGB_RGB_FUNDUS.jpg)

### Car
![alt text](https://github.com/reshalfahsi/GGB/raw/master/docs/img/GGB_RGB_TESLA.jpg)
