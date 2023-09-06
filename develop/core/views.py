from django.views.generic import TemplateView

#--------------
# VIEWS - Views for your app
#--------------

class IndexView(TemplateView):
    template_name = "core/index.html"
