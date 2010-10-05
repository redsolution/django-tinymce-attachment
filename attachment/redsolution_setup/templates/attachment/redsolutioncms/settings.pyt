# ---- django-tinymce-attachment ----

try:
    TINYMCE_DEFAULT_CONFIG
except NameError:
    TINYMCE_DEFAULT_CONFIG = {}

TINYMCE_DEFAULT_CONFIG.update({
    'external_image_list_url': 'images/',
    'external_link_list_url': 'links/',
})

INSTALLED_APPS += ['attachment', 'imagekit']

ATTACHMENT_FOR_MODELS = [{% for model in attachment_settings.models.all %}
    '{{ model.model }}',{% endfor %}
]

ATTACHMENT_LINK_MODELS = [{% for link in attachment_settings.links.all %}
    '{{ link.model }}',{% endfor %}
]
