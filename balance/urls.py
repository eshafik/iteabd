from django.urls import path

from . import views

app_name="balance"

urlpatterns=[
    path('active_members/', views.active_members, name="active_members"),
    path('add_balance/<slug:username>', views.add_balance, name="add_balance"),
    path('org_edit/', views.org_edit, name='org_edit'),
    path('org_detail/', views.org_detail, name='org_detail'),
    path('transaction/', views.transaction, name='transaction'),
    path('get_transaction/', views.GeneratePdf.as_view(), name='get_ransaction'),
    path('org_transaction/', views.org_transaction, name='org_transaction'),
    path('my_transaction/', views.personal_transaction, name='my_transaction'),
    path('investor_form/', views.investor_add_balance, name='investor_form'),
    path('investor_trans/', views.investor_transaction, name='investor_trans'),
]