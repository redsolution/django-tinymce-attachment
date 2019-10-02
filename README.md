
# django tinymce attachment

Open source images management system based on the Django framework.

## Features
- Work with images, files and archives.
- integration with TinyMCE editor.
- Easy to connect to any model.
- Resize, crop, upscale and add filters to images.

## Requirements

- Python 2.7
- Django 1.11.*
- django-tinymce 2.6.0
- django-imagekit 0.3.3
- django-classy-tags >=0.3,<=0.9.0

## Installation and basic usage


1. Install package

    ``git+git://github.com/oldroute/django-tinymce-attachment@1.11``

2. Create application ``custom_attachment``. Add next files to  app:

	**resizes.py**:

    ```python
    from imagekit.processors import Resize

    class ResizeThumb(Resize): # required resize
        width = 172
        height = 172

    class ResizeDisplay(Resize):  # required resize
        width = 1200
        height = 900

    class ResizeImg384x288(Resize): # optional resize
        width = 384
        height = 288
        crop = True
        upscale = True

    class ResizeImgAutox408(Resize):  # optional resize
        height = 408

    ```
	"Resize" it is processor for change image size. Which has the following parameters:
    - **width** - width limit (*default: None*).
    - **height** - height limit (*default: None*).
    - **crop** - crop image to maintain aspect ratio for specified width and height (*default: False*).
    - **upscale** - increase image size to maintain aspect ratio for specified width and height (*default: False*).

    **ikspecs.py**:

    ```python
    from imagekit.specs import ImageSpec
    from .resizes import *

    class Thumb(ImageSpec):
    	processors = [ResizeThumb]

    class Display(ImageSpec):
    	processors = [ResizeDisplay]

    class Img384x288(ImageSpec):
    	processors = [ResizeImg384x288]
		quality = 80

    class ImgAutox408(ImageSpec):
    	processors = [ResizeImgAutox408]

    ```
    Image specifications is a set of processors.  Which has the following parameters:
    - **processors** - list of image processors (*deafault: empty list*)
    - **quality** - value in range 0 to 100 (source image have 100 quality). You can lower the jpeg image quality for optimization image size. **You cannot reduce the png image file-size in this way** (*deafault: 70*)

3. Configure your settings file:

	- **ATTACHMENT_FOR_MODELS** - list of models for connecting images and files (*default: empty list*)
	- **ATTACHMENT_UPLOAD_DIR** - folder in the media root for storing attachment files (*default: 'upload/attachment/source'*)
	- **ATTACHMENT_CACHE_DIR** - folder in the media root for storing image versions (*default*: 'upload/attachment/cache')
	- **ATTACHMENT_IKSPECS** - file with specifications of image versions (*default*: 'attachment.ikspecs')
	- **ATTACHMENT_EXTRA_IMAGES, ATTACHMENT_EXTRA_FILES** - count of extra inline images/files for connected models (*default: 3*)
	- **ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE, ATTACHMENT_MAX_FILE_UPLOAD_SIZE** - limit in bytes for uploaded images/files (*default*: None). Pay attention to Django variables: **FILE_UPLOAD_MAX_MEMORY_SIZE** and **FILE_UPLOAD_PERMISSIONS**.
	- **GROUP_IMAGES** - Add to attachments extra field "group" (*default: True*).
	- **ATTACHMENT_IMAGE_ROLES** - list fixed image roles - for example "gallery", "caption"(*default: False*)
	- **ATTACHMENT_LINK_MODELS** - list of models to be listed in link-list TinyMCE (*default: empty list*)
	- **ATTACHMENT_SPECS_FOR_TINYMCE** - list specifications for TinyMCE editor (*default*: empty list).
    For example we need connect attachments to "Page" model.

    Simple settings configuration:

    ```python
    # attachments
    INSTALLED_APPS += ['unidecode', 'imagekit', 'attachment', '<PROJECT_ROOT>.custom_attachment']
    ATTACHMENT_FOR_MODELS = [
        #'<app>.<model>',
        'pages.Page',
    ]
    ATTACHMENT_LINK_MODELS = [
        #'<app>.<model>',
        'pages.Page',
    ]
    FILE_UPLOAD_MAX_MEMORY_SIZE = '2621440'
	FILE_UPLOAD_PERMISSIONS = 0644
    ATTACHMENT_EXTRA_IMAGES = 0
	ATTACHMENT_EXTRA_FILES = 0
    ATTACHMENT_IKSPECS = '<PROJECT_ROOT>.custom_attachment.ikspecs'
	ATTACHMENT_IMAGE_ROLES = ['gallery', 'caption']

	# TinyMCE
    INSTALLED_APPS += ['tinymce']
    TINYMCE_DEFAULT_CONFIG = {
    'mode': 'exact',
    'theme': 'advanced',
    'relative_urls': False,
    'width': 1024,
    'height': 300,
    'skin': 'o2k7',
    'plugins': 'table,advimage,advlink,inlinepopups,preview,media,searchreplace,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras',
    'theme_advanced_buttons1': 'justifyleft,justifycenter,justifyright,|,bold,italic,underline,strikethrough,|,sub,sup,|,bullist,numlist,|,outdent,indent,|,formatselect,removeformat,cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,link,unlink,anchor,image,media,charmap,|,visualchars,nonbreaking',
    'theme_advanced_buttons2': 'visualaid,tablecontrols,|,blockquote,del,ins,|preview,fullscreen,|,code',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'valid_elements': '*[*]',
    'extended_valid_elements': '*[*]',
    'custom_elements': 'noindex',
    'external_image_list_url': 'images/',
    'external_link_list_url': 'links/',
    'paste_remove_styles': 'true',
    'paste_remove_styles_if_webkit': 'true',
    'paste_strip_class_attributes': 'all',
    'plugin_preview_width': '900',
    'plugin_preview_height': '800',
    'accessibility_warnings': 'false',
    'theme_advanced_resizing': 'true',
    'content_style': '.mcecontentbody{font-size:14px;}',
    }

	```
4. Add urlpattern to main urls.py:

    ```python
    from django.views.static import serve
	from django.conf import settings
    from django.contrib import admin
	from django.conf.urls import url, include

    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^', include('attachment.urls')), # before admin urls
        url(r'^admin/', admin.site.urls),
        url(r'^tinymce/', include('tinymce.urls')),
        # ...
    ]
    ```
5. Call attachments in template:

    Example №1. Get page images/files:
    ```html
	{% load attachment_tags %}

    {% get_images for current_page as images %}
    {% get_files for current_page as files %}
    ```

    Example №2. Show page images/files:
	```
	{% load attachment_tags %}

	{% show_images for current_page %}
	{% show_files for current_page %}
    ```
	To customize attachments ``show.html`` template, stick to the following template structure:
	- templates/
    	- attachment/
        	- show.html

    Example №3. Image specifications:
	```html
    {% load attachment_tags %}

    {% get_images for current_page as images %}
    {% for image in images %}
    	<picture>
        	<source srcset="{{ image.display.url }}" media="(min-width: 1216px)"/>
            <source srcset="{{ image.imgautox408.url }}" media="(min-width: 1024px)"/>
            <source srcset="{{ image.img384x288.url }}" media="(min-width: 768px)"/>
         	<source srcset="{{ image.thumb.url }}" media="(min-width: 320px)"/>
            <img src="{{ image.thumb.url }}" alt="{{ image.title }}"/>
        </picture>
    {% endfor %}
	```

6. Apply migrations, run local server and add attachments in admin

    ```python
    python manage.py migrate
    python manage.py runserver
    ```

## Advanced usage

#### Processors

We have several processors from the box:

- **BottomCenterWatermark**
- **BottomLeftWatermark**
- **BottomRightWatermark**
- **CenterWatermark**
- **AroundWatermark** - repeated throughout the photo.
- **GrayScale** - image discoloration.

**Example:**

1. Put ``watermark.png`` image to your images directory
2. Create ``<PROJECT_ROOT>/custom_attachment/processors.py`` with the following contents:

    ```python
    from os.path import join
    from django.conf import settings
    from attachment.processors import BottomLeftWatermark

    STATIC_PATH = join(settings.PROJECT_ROOT, 'static') if settings.DEBUG else settings.STATIC_ROOT

    class BLWatermark(BottomLeftWatermark):

        image_path = join(STATIC_PATH, 'img', 'watermark.png')
        opacity = 0.7
        left = 0
        bottom = 50
    ```
3. Add Watermark processor to image specification in ``<PROJECT_ROOT>/custom_attachment/ikspecs.py``:

    ```python
    from imagekit.specs import ImageSpec
    from .resizes import *
    from .processors import BLWatermark
    from attachment.processors import GrayScale

    class WatermarkDisplay(ImageSpec):
    	processors = [ResizeDisplay, BLWatermark]

    class GrayScaleDisplay(ImageSpec):
    	processors = [ResizeDisplay, GrayScale]
    ```
4. To add a new image specifications to the TinyMCE editor update ``settings.py``:

  	```
    ATTACHMENT_SPECS_FOR_TINYMCE = ['watermarkdisplay', 'grayscaledisplay']
    ```
5. Call new image specifications in template:

	```html
    {% load attachment_tags %}

    {% get_images for current_page as images %}
    {% for image in images %}
        <img src="{{ image.watermarkdisplay.url }}"/>
        <img src="{{ image.grayscaledisplay.url }}"/>
    {% endfor %}
	```
#### Commands

**update_cache** - сommand updates images of specified specification or model. parameters:
- **-s** - specify image specification, for example:

	```
	python manage.py update_cache -s img384x288
    ```
- **-m** - specify image model *(optional, default attachment.AttachmentImage )*. For example:
	```
    python manage.py update_cache -s img384x288 -m attachment.AttachmentImage
    ```
#### Custom application based on attachments

For example, we need the Sliders app, for use attachments backend follow next steps:

**models.py**
```python
from imagekit.models import ImageModel
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from attachment.fields import ImagePreviewField
from attachment import settings


class Slide(ImageModel):

    class IKOptions:
        spec_module = settings.ATTACHMENT_IKSPECS
        cache_dir = settings.ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = ImagePreviewField(widget_type='horizontal', upload_to=settings.ATTACHMENT_UPLOAD_DIR)


class Slider(models.Model):

    slides = GenericRelation(Slide)
```
'ImagePrviewField' has following attributes:
- **widget_type** - set specified widget template, can take the value **horisontal**, **vertical** or None (*default: None*)
- **upload_to** - directory to upload image