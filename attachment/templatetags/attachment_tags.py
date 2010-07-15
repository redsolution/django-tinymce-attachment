# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.template.loader import render_to_string
from attachment.models import AttachmentImage, AttachmentFile

INTENT_ATTACHMENTS = 'attachments'
INTENT_IMAGES = 'images'
INTENT_FILES = 'files'
INTENTS = [INTENT_ATTACHMENTS, INTENT_IMAGES, INTENT_FILES]

def get_list(intent, object, context):
    result = []
    object = template.Variable(object).resolve(context)
    if object is None:
        return result
    if intent in [INTENT_ATTACHMENTS, INTENT_IMAGES]:
        result += [attachment for attachment in AttachmentImage.objects.filter(
            content_type=ContentType.objects.get_for_model(object.__class__),
            object_id=object.id)]
    if intent in [INTENT_ATTACHMENTS, INTENT_FILES]:
        result += [attachment for attachment in AttachmentFile.objects.filter(
            content_type=ContentType.objects.get_for_model(object.__class__),
            object_id=object.id)]
    return result

register = template.Library()

class ShowAttachments(template.Node):
    def __init__(self, intent, object):
        self.intent = intent
        self.object = object

    def render(self, context):
        attachments = get_list(self.intent, self.object, context)
        return render_to_string('attachment/show.html', {
            'attachments': attachments,
        }, context_instance=template.RequestContext(context.get('request', HttpRequest())))

def show_attachments(parser, token):
    """Show attachments for object"""
    splited = token.split_contents()
    if len(splited) != 3 or splited[0].split('_')[1] not in INTENTS or splited[1] != 'for':
        raise template.TemplateSyntaxError, "Invalid syntax. Use ``{% show_<attachments|images|files> for <object> %}``"
    return ShowAttachments(splited[0].split('_')[1], splited[2])

for intent in INTENTS:
    register.tag('show_%s' % intent, show_attachments)


class GetAttachments(template.Node):
    def __init__(self, intent, object, variable):
        self.intent = intent
        self.object = object
        self.variable = variable

    def render(self, context):
        context[self.variable] = get_list(self.intent, self.object, context)
        return u''

def get_attachments(parser, token):
    """Show attachments for object"""
    splited = token.split_contents()
    if len(splited) != 5 or splited[0].split('_')[1] not in INTENTS or splited[1] != 'for' or splited[3] != 'as':
        raise template.TemplateSyntaxError, "Invalid syntax. Use ``{% get_<attachments|images|files> for <object> as <variable> %}``"
    return GetAttachments(splited[0].split('_')[1] , splited[2], splited[4])

for intent in INTENTS:
    register.tag('get_%s' % intent, get_attachments)