from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    path('create_post/', views.create_post,
         name='create_post'),
    path('post_list/', views.post_list,
         name='post_list'),
    path('my_published_post/', views.my_published_post,
         name='my_published_post'),
    path('post_edit/<int:id>/', views.post_edit,
         name='post_edit'),
    path('post_delete/<int:id>/', views.post_delete,
         name='post_delete'),
    path('draft_list/', views.draft_list,
         name='draft_list'),
    path('yarn/', views.yarn,
         name='yarn'),
    path('fabric/', views.fabric,
         name='fabric'),
    path('wet/', views.wet,
         name='wet'),
    path('apparel/', views.apparel,
         name='apparel'),
    path('printing/', views.printing,
         name='printing'),
    path('merchandising/', views.merchandising,
         name='merchandising'),
    path('others/', views.others,
         name='others'),
    path('notice/', views.notice,
         name='notice'),
    path('search/', views.post_search,
         name='post_search'),
    re_path(r'tag/(?P<tag_slug>([^/]+))/$', views.post_list, name='post_list_by_tag'),  
#     path('post_detail/<int:year>/<int:month>/<int:day>/<int:id>/',
#          views.post_detail,
#          name='post_detail'),
     path('post_detail/<int:id>/',
         views.post_detail,
         name='post_detail'),
]