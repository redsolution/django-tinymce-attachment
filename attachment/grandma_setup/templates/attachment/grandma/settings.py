# django-tinymce-attachment
INSTALLED_APPS += ['attachment']

ATTACHMENT_FOR_MODELS = [{% for model in attachment_settings.models.all %}
    {'model': '{{ model.model }}',},{% endfor %}
]

ATTACHMENT_LINK_MODELS = [{% for link in attachment_settings.links.all %}
    {'model': '{{ link.model }}',},{% endfor %}
]
