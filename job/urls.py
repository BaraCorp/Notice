"""job URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from job import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^new_user/$', views.new_user, name='new-user'),
    url(r'^new_organization/$', views.new_organization,
        name='new-organization'),
    url(r'^new_notice/(?P<pk_org>\w+)$', views.add_notice, name='add-notice'),
    url(r'^notice_change/(?P<pk_notice>\w+)$', views.notice_change,
        name='notice-change'),
    url(r'^notice_view/(?P<pk_notice>\w+)$', views.notice_view,
        name='notice-view'),
    url(r'^user_manager/$', views.user_manager, name='user-manager'),
    url(r'^organization_manager/$', views.organization_manager,
        name='organization-manager'),
    url(r'^organization_view/(?P<pk>\w+)$', views.organization_view,
        name='organization-view'),
    url(r'^user_change/(?P<pk>\w+)', views.user_change, name='user-change'),
    url(r'^organization_change/(?P<pk>\w+)', views.organization_change,
        name='organization-change'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
