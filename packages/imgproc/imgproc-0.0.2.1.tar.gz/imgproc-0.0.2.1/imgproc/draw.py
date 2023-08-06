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
from PIL import ImageDraw
from imgproc.image import Image


def polygon(src: Image = None, points: list = None, fill: tuple = (255, 0, 0, 125), outline: int = 1) -> Image:
    """
    Draw polygon into an image.
    :param src:     source image.
    :param points:  points of polygon.
    :param fill:    fill color of polygon.
    :param outline: outline stoke of polygon.
    :return:        drawn image.
    """
    # Validate source.
    assert isinstance(src, Image), 'Image is undefined.'
    # Draw polygon.
    draw = ImageDraw.Draw(src._image, 'RGBA' if len(fill) > 3 else src.color)
    draw.polygon(points, fill, outline)
    # Return result.
    return src
