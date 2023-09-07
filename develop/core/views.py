from django.views.generic import TemplateView

# --------------
# VIEWS - Views for your app
# --------------


class IndexView(TemplateView):
    template_name = "core/index.html"


class TestView(TemplateView):
    template_name = "test_page.html"
