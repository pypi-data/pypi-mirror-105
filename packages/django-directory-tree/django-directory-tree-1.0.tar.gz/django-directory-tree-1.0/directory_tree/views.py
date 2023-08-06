import json

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils.directory_tree import DirectoryTree

class DirectoryTreeView(TemplateView):

    template_name = 'directory_tree/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL
        if not media_root or not media_url:
            context['error'] = "error : undefind MEDIA_ROOT or MEDIA_URL in setting"
            return context

        pattern = r".*"
        obj = DirectoryTree(media_root, pattern=pattern)
        context['folder_tree'] = json.dumps(obj.dict_file)
        return context