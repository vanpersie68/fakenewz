from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from rest_framework import permissions
import os
from pathlib import Path
from . import consumers
from . import focus
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws/test/(?P<id>[0-9]|[1-9][0-9]|100)/$', consumers.MyConsumer.as_asgi()),
    url(r'^ws/focus/', focus.Focus.as_asgi()),
]

schema_view = get_schema_view(
    openapi.Info(
        title="CS63 API",
        default_version='v1',
        description="Welcome to CS63 survey platform",
        terms_of_service="",
        contact=openapi.Contact(email="kjin9446@uni.sydney.edu.au"),
        license=openapi.License(name="Apache license"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=()
)
BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('surveybuilder.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('survey/', include('survey.urls')),
   # path('status/', django_core.views.status),
    path('emailInfo/', include('emailInfo.urls')),
    path('api/st/', include('surveytaker.urls')),
    *static('/static', document_root=os.path.join(BASE_DIR, 'static/static')),
    *static('/upload', document_root=os.path.join(BASE_DIR, 'static/upload')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('<path:path>', TemplateView.as_view(template_name='index.html')),
    path('crontab/', include('crontab.surveyLifecycle')),
]
# urlpatterns += static('/static', document_root=os.path.join(BASE_DIR, 'static/static'))

# urlpatterns += static('/', document_root=os.path.join(BASE_DIR, 'static'))
