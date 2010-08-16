# django-tinymce-attachment

TINYMCE_DEFAULT_CONFIG = {
    'mode': 'exact',
    'theme': 'advanced',
    'relative_urls': False,
    'width': 600,
    'height': 300,
    'plugins': 'table,advimage,advlink,inlinepopups,preview,media,searchreplace,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras',
    'theme_advanced_buttons1': 'fullscreen,|,bold,italic,underline,strikethrough,|,sub,sup,|,bullist,numlist,|,outdent,indent,|,formatselect,removeformat',
    'theme_advanced_buttons2': 'cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,link,unlink,anchor,image,media,charmap,|,visualchars,nonbreaking',
    'theme_advanced_buttons3': 'visualaid,tablecontrols,|,blockquote,del,ins,|,preview,code',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'content_css': '/media/css/tinymce.css',
    'extended_valid_elements': 'noindex',
    'custom_elements': 'noindex',
    'external_image_list_url': 'images/',
    'external_link_list_url': 'links/',
}
TINYMCE_COMPRESSOR = True

INSTALLED_APPS += ['attachment', 'imagekit']

ATTACHMENT_FOR_MODELS = [{% for model in attachment_settings.models.all %}
    '{{ model.model }}',{% endfor %}
]

ATTACHMENT_LINK_MODELS = [{% for link in attachment_settings.links.all %}
    '{{ link.model }}',{% endfor %}
]

