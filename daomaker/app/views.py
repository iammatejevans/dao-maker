import datetime
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.generic import ListView

from app.models import Task
from datetime import datetime


class ParseURLAjax(View):
    def get(self, request, *args, **kwargs):
        return render(request, "url.html", {})

    def post(self, request, *args, **kwargs):
        url = request.POST.get("url", "")

        try:
            # validate url
            val = URLValidator()
            val(url)

            # parse data
            external_sites_html = urlopen(url).read()
            soup = BeautifulSoup(external_sites_html, "html.parser")

            site_name = urlparse(url).hostname
            title = soup.title.text
            image = ""
            desc = ""

            for meta in soup.findAll("meta"):
                title = self.get_meta_property(meta, "og:title", title) if not title else title
                image = self.get_meta_property(meta, "og:image", image) if not image else image
                desc = self.get_meta_property(meta, "og:description", desc) if not desc else desc
                if title and image and desc:
                    break

            # save data
            Task.objects.create(
                url=url,
                title=title if title else None,
                description=desc if desc else None,
                site_name=site_name if site_name else None,
                image_url=image if image else None,
                created=datetime.today().date(),
            )

            return HttpResponse("success")

        except (URLError, ValidationError):
            return HttpResponse("url not valid")

    @staticmethod
    def get_meta_property(meta, property_name, default_value=""):
        if 'property' in meta.attrs and meta.attrs['property'] == property_name:
            return meta.attrs['content']
        return default_value


class GetData(ListView):
    model = Task
    template_name = "list.html"
