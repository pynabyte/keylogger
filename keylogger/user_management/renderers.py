from rest_framework.renderers import JSONRenderer

class ApiRenderer(JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(data,accepted_media_type, renderer_context)
