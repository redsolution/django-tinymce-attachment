from django.core.management.base import BaseCommand, CommandError
from django.apps import apps as django_apps
from imagekit.models import ImageModel
import sys


class Command(BaseCommand):
    help = ('Update Imagekit cached files for spec.')

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', action='store', type=str, dest='model', help='Model name "attachment.AttachmentImage" ', default='attachment.AttachmentImage'),
        parser.add_argument('-s', '--spec', action='store', type=str, dest='spec', help='Spec name'),

    can_import_settings = True

    def handle(self, *args, **options):
        try:
            app_label, model_name = tuple(options.get('model').split('.'))
        except ValueError:
            raise CommandError('Wrong format for option --model. Example: "app_label.model_name" ')
        try:
            app = django_apps.get_app_config(app_label)
        except LookupError:
            raise CommandError('No installed app with label %s' % app_label)
        try:
            model = app.get_model(model_name)
        except LookupError:
            raise CommandError("App %s doesn't have a %s model." % (app_label, model_name))

        if not issubclass(model, ImageModel):
            raise CommandError('%s model is not subclass ImageModel' % app_label)
        spec = options.get('spec')
        items = model.objects.all()
        count = len(items)
        for i, obj in enumerate(items):
            prop = getattr(obj, spec, None)
            if prop is not None:
                if prop._exists():
                    prop._delete()
                    prop._create()
            else:
                raise CommandError("Model %s doesn't have spec %s" % (model_name, spec))
            sys.stdout.write("\rUpdate cache....%s%%" % (int(float(i + 1) / count * 100),))
            sys.stdout.flush()
        sys.stdout.write('\n')