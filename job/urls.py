
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
    url(r'^user_new/$', views.user_new, name='new-user'),
    url(r'^user_manager/$', views.user_manager, name='user-manager'),
    url(r'^user_change/(?P<pk>\w+)', views.user_change, name='user-change'),
    url(r'^notice_new/(?P<pk_org>\w+)$', views.add_notice, name='add-notice'),
    url(r'^call_for_tender_new/(?P<pk_org>\w+)$', views.call_for_tender_new, name='call-for-tender-new'),
    url(r'^snotice_validated/(?P<pk>\w+)$', views.snotice_validated, name='snotice-validated'),
    url(r'^snotice_unvalidated/(?P<pk>\w+)$', views.snotice_unvalidated, name='snotice-unvalidated'),
    url(r'^datajson/(?P<obj>\w+)$', views.data_json, name='data-json'),
    url(r'^not_clean_manager/$', views.not_clean_manager, name='not-clean-manager'),
    # url(r'^clean_call_tend/(?P<url>.*)$', views.clean_call_tender, name='clean-call-tender'),
    url(r'^notice_change/(?P<pk_notice>\w+)$', views.notice_change, name='notice-change'),
    url(r'^notice_view/(?P<pk_notice>\w+)$', views.notice_view, name='notice-view'),
    url(r'^organization_new/$', views.organization_new, name='new-organization'),
    url(r'^small_notice_manager/$', views.small_notice_manager, name='small-notice-manager'),
    url(r'^small_notice_view/$', views.small_notice_view, name='small-notice-view'),
    url(r'^organization_manager/$', views.organization_manager, name='organization-manager'),
    url(r'^organization_view/(?P<pk>\w+)$', views.organization_view, name='organization-view'),
    url(r'^organization_change/(?P<pk>\w+)', views.organization_change, name='organization-change'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
