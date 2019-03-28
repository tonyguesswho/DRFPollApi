from django.urls import re_path, include, path
from .views import ChoicesList, CreateVote, PollsViewset,CreateUser
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',PollsViewset, base_name='polls')

urlpatterns = [
    # path('', PollsList.as_view(), name='polls_list'),
    # path('<int:pk>/', PollsDetail.as_view(), name='polls_details'),
    path('<int:pk>/choices/',ChoicesList.as_view(), name='choice_list' ),
    path('<int:pk>/choices/<int:choice_pk>/vote/',CreateVote.as_view(), name='create_view'),
    # path('users/',CreateUser.as_view(), name='create_user')
]

urlpatterns+=router.urls