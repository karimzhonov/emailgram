from django.urls import path
from .views import *

urlpatterns = [
    path('admins/', UserAdminsListView.as_view()),
    path('user/', UserGetOrCreate.as_view()),
    path('mail/', MailGet.as_view()),
    path('mails/', MailsGet.as_view()),
    path('newmail/', CreateMail.as_view()),
]