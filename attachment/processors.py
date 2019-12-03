# -*- coding: utf-8 -*-
from imagekit.processors import ImageProcessor
from imagekit.lib import *


class GrayScale(ImageProcessor):

    """ image discoloration """

    @classmethod
    def process(cls, img, fmt, obj):
        img = img.convert('L')
        return img, fmt


class WatermarkBase(ImageProcessor):

    image_path = None
    opacity = 1
    top = 0
    left = 0
    right = 0
    bottom = 0

    @classmethod
    def _apply_opacity(cls, im):
        assert 0 <= cls.opacity <= 1, 'opacity not in range 0..1'
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(cls.opacity)
        im.putalpha(alpha)
        return im

    @classmethod
    def _apply_mark(cls, img, mark):
        # abstract interface
        pass

    @classmethod
    def process(cls, img, fmt, obj):

        try:
            mark = Image.open(cls.image_path)
        except IOError as e:
            raise IOError('Unable to open watermark source image %s: %s' % (cls.image_path, e))

        mark = cls._apply_opacity(mark)
        im = cls._apply_mark(img, mark)
        return im, fmt


class BottomRightWatermark(WatermarkBase):

    """ positioning watermark to the bottom right """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        x = img.size[0] - mark.size[0] - cls.right
        y = img.size[1] - mark.size[1] - cls.bottom
        layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)


class BottomCenterWatermark(WatermarkBase):

    """ positioning watermark to the bottom center """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        x = (img.size[0] - mark.size[0]) / 2
        y = img.size[1] - mark.size[1] - 40
        layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)


class BottomLeftWatermark(WatermarkBase):

    """ positioning watermark to the bottom left """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        x = cls.left
        y = img.size[1] - mark.size[1] - cls.bottom
        layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)


class AroundWatermark(WatermarkBase):

    """ positioning watermark around the photo """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        for y in range(0, img.size[1], mark.size[1]):
            for x in range(0, img.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)


class CenterWatermark(WatermarkBase):

    """ positioning watermark in the center """

    @classmethod
    def _apply_mark(cls, img, mark):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        x = (img.size[0] - mark.size[0]) / 2
        y = (img.size[1] - mark.size[1]) / 2
        layer.paste(mark, (x, y))
        return Image.composite(layer, img, layer)
