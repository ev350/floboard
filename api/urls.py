"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="FloBoard API",
        default_version='v1',
        description="Euan's Project Board API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="euan-cowie@hotmail.co.uk"),
        license=openapi.License(name="BSD License"),
    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Boards
    path('boards/', views.BoardList.as_view(), name='board_list'),
    path('boards/<int:board_pk>/', views.BoardDetail.as_view(), name='board_detail'),

    # Columns
    path('boards/<int:board_pk>/columns/', views.ColumnList.as_view(), name='column_list'),
    path('boards/<int:board_pk>/columns/<int:position>/', views.ColumnDetail.as_view(), name='column_detail'),

    # Cards
    path('boards/<int:board_pk>/cards/', views.CardList.as_view(), name='card_list'),
    path('boards/<int:board_pk>/cards/<int:card_pk>/', views.CardDetail.as_view(), name='card_detail'),

    # Labels
    path('boards/<int:board_pk>/labels/', views.LabelList.as_view(), name='label_list'),
    path('boards/<int:board_pk>/labels/<int:label_pk>/', views.LabelDetail.as_view(), name='label_detail'),

    # Comments
    path('boards/<int:board_pk>/cards/<int:card_pk>/comments/', views.CommentList.as_view(), name='card_comment_list'),
    path('boards/<int:board_pk>/cards/<int:card_pk>/comments/<int:comment_pk>/', views.CommentDetail.as_view(),
         name='card_comment_detail'),

    # Swagger Docs
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

# Notes: In my opinion, it is not necessary to have the /columns/ in a path such as boards/1/columns/2/cards/3/comments
#        because it just confuses the user (and me), thus will not be added unless it becomes necessary to single out
#        the columns of each board.
#
# Examples:
#
# path('boards/<int:board_pk>/columns/<int:position>/cards/', views.CardList.as_view(), name='card_column_list'),
# path('boards/<int:board_pk>/columns/<int:position>/cards/<int:card_pk>/', views.CardDetail.as_view(),
#      name='card_column_detail'),
# path('boards/<int:board_pk>/columns/<int:position>/cards/<int:card_pk>/comments', views.CommentList.as_view(),
#      name='card_column_comments'),
