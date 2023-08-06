# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 Hieu Tr. Pham
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage, ImageOps as PILImageOps


class Image:
    """
    This class is used to handle image.
    """

    @property
    def array(self):
        """
        Return image as numpy array.
        :return:    numpy array
        """
        return np.squeeze(np.asarray(self._image, dtype=np.uint8))

    @property
    def color(self):
        """
        Return image color.
        :return:    image color.
        """
        return self._color

    def __init__(self, src = None, gray: bool = False):
        """
        Construct image from source.
        :param src:     image source.
        :param gray:    load as grayscale.
        """
        # Initialize
        self._image, self._color = None, None
        # Load image if source exists.
        if src is not None:
            self.load(src=src, gray=gray)

    def load(self, src = None, gray: bool = False):
        """
        Load image from source.
        :param src:     image source.
        :param gray:    load as grayscale.
        :return:        loaded image.
        """
        # Load from array data.
        if isinstance(src, (list, np.ndarray)):
            self._image = PILImage.fromarray(np.squeeze(np.asarray(src, dtype=np.uint8)))
        # Other cases as string.
        elif isinstance(src, str):
            # Load from file path.
            if os.path.isfile(src):
                self._image = PILImage.open(src)
        # Adjust color
        if gray:
            self._image = self._image.convert('L')
            self._color = 'gray'
        else:
            self._image = self._image.convert('RGB')
            self._color = 'rgb'
        # Return result.
        return self

    def save(self, file: str = 'untitled.jpg'):
        """
        Save image to file.
        :param file:    file to save image.
        :return:        saved image.
        """
        # Save image.
        self._image.save(file)
        # Return result.
        return self

    def show(self, handler: str = 'matplotlib'):
        """
        Show image.
        :param handler: handler of show function.
        :return:        showed image.
        """
        # Matplotlib handler.
        if handler == 'matplotlib':
            plt.imshow(self._image)
            plt.show()
        # Otherwise.
        else:
            self._image.show()
        # Return result.
        return self

    def resize(self, size: tuple = (224, 224)):
        """
        Resize image to desired size.
        :param size:    desired size.
        :return:        resized image.
        """
        # Resize image.
        self._image = self._image.resize(size=size, resample=PILImage.BILINEAR)
        # Return result.
        return self

    def square_pad(self):
        """
        Convert image into square with zero paddings.
        :return:    squared image.
        """
        # Calculate elements.
        h, w = self._image.size
        max_edge = max(h, w)
        dh, dw = max_edge - h, max_edge - w
        # Perform padding.
        padding = (dh // 2, dw // 2, dh - (dh // 2), dw - (dw // 2))
        self._image = PILImageOps.expand(self._image, padding)
        # Return result.
        return self
