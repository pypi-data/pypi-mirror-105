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

        base_dir = settings.MEDIA_ROOT
        pattern = r".*"
        obj = DirectoryTree(base_dir, pattern=pattern)
        context['folder_tree'] = json.dumps(obj.dict_file)        
        return context