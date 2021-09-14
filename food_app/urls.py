from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('restaurants',views.success),#disabling it for the wall to work
    path('logout',views.logout),
    path('restaurants/create',views.createrestaurants),
    path('restaurants/all',views.all),
    path('restaurants/<int:rest_id>',views.onerestaurant),
    path('reviews/create/<int:rest_id>',views.createreview),
    path('restaurants/userprofile/<int:user_id>', views.oneuser),
    path('uploadimage/<int:user_id>',views.uploadimage),
    path('restaurants/delete/<int:rest_id>', views.deleterest),
    path('restaurants/review/delete/<int:review_id>/<int:rest_id>', views.deletereview),
    path('restaurants/review/<int:review_id>/<int:rest_id>',views.updatereviewpage),
    path('restaurants/review/update/<int:review_id>/<int:rest_id>', views.updatereview),
]
