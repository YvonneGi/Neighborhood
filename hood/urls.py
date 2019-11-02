from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    # url(r'^search/', views.search_results, name='search_results'),
    # url(r'^explore/', views.explore, name = 'explore'),
    url(r'^accounts/profile/(\d+)', views.profile, name = 'profile'),
    url(r'^accounts/edit-profile/', views.edit_profile, name = 'edit-profile'),
    url(r'^new/hood$', views.new_hood, name='new_hood'),
    url(r'^join_hood/(\d+)', views.join_hood, name='join_hood'),
    url(r'^leave_hood/(\d+)', views.leave_hood, name='leave_hood'),
    url(r'^new/biz$', views.new_biz, name='new_biz'),
    url(r'^new/post$', views.new_post, name='new_post'),
    url(r'^user/(?P<username>\w+)', views.user_profile, name='user_profile'),
   
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)