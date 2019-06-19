from imagekit.processors import ImageProcessor
from imagekit.lib import *


class WatermarkPositioning(object):
    def __init__(self, opacity=0.5, position=(0, 0)):
        self.position = position
        self.opacity = opacity

    def render(self, im, mark):
        layer, mark, im = self.prepare(im, mark)
        layer = self.positioning(mark, im, layer)
        # composite the watermark with the layer
        return Image.composite(layer, im, layer)

    def prepare(self, im, mark):
        if self.opacity < 1:
            mark = self._reduce_opacity(mark)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        return layer, mark, im

    def _reduce_opacity(self, im):
        """Returns an image with reduced opacity."""
        assert self.opacity >= 0 and self.opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        im.putalpha(alpha)
        return im

    def positioning(self, mark, im, layer):
        layer.paste(mark, self.position)
        return layer


class ResizedWatermarkPositioning(WatermarkPositioning):
    class Meta:
        abstract = True

    def __init__(self, opacity=0.5, offset=0):
        self.opacity = opacity
        self.offset = offset

    def __resize_watermark(self, im, mark):
        ratio = min(
            float((im.size[0])) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        return mark.resize((w, h))

    resize_watermark = __resize_watermark

    def prepare(self, im, mark):
        layer, mark, im = WatermarkPositioning.prepare(self, im, mark)
        mark = self.resize_watermark(im, mark)
        return layer, mark, im

    def positioning(self, mark, im, layer):
        raise NotImplementedError


class TileWatermarkPositioning(ResizedWatermarkPositioning):
    def positioning(self, mark, im, layer):
        x_offset = -1 * self.offset
        for y in range(0, im.size[1], im.size[1]/3):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x + x_offset, y + im.size[1]/6))
            x_offset *= -1
        return layer


class ScaleWatermarkPositioning(ResizedWatermarkPositioning):
    def positioning(self, mark, im, layer):
        layer.paste(mark,
                    ((im.size[0] - mark.size[0]) / 2,
                     (im.size[1] - mark.size[1]) / 2))
        return layer


class CenterWatermarkPositioning(ScaleWatermarkPositioning):
    def __resize_watermark(self, im, mark):
        if mark.size[0] >= im.size[0] or mark.size[1] >= im.size[1]:
            return super(CenterWatermarkPositioning, self).__resize_watermark()
        return mark
    resize_watermark = __resize_watermark


class BottomWatermarkPositioning(ResizedWatermarkPositioning):
    def __resize_watermark(self, im, mark):
        if (mark.size[1] > im.size[1]/5):
            h = im.size[1]/5
            w = mark.size[0] * h / mark.size[1]
            return mark.resize((w, h))
        return mark
    resize_watermark = __resize_watermark

    def positioning(self, mark, im, layer):
        layer.paste(mark, (self.offset, 
                           (im.size[1] - mark.size[1] - self.offset)))
        return layer


class BottomCenterPositioning(BottomWatermarkPositioning):
    def positioning(self, mark, im, layer):
        layer.paste(mark, 
                    ((im.size[0] - mark.size[0]) / 2,
                     (im.size[1] - mark.size[1] - self.offset)))
        return layer


class Watermark(ImageProcessor):
    image_path = None
    position = WatermarkPositioning(opacity=0.8)

    @classmethod
    def process(self, image, format, obj=None):
        try:
            mark = Image.open(self.image_path)
        except IOError, e:
            raise IOError('Unable to open watermark source image %s: %s' % \
                          (self.image_path, e))
        try:
            im = self._apply_watermark(image, mark)
        except Exception, e:
            print e
        return im, format

    @classmethod
    def _apply_watermark(self, image, mark):
        layer, mark, im = self.position.prepare(image, mark)
        layer = self.position.positioning(mark, image, layer)
        # composite the watermark with the layer
        return Image.composite(layer, im, layer)
