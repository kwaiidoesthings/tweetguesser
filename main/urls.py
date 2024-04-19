# image_guess/urls.py
from django.urls import path
from . import views as m

urlpatterns = [
    path('guess/', m.show_image, name='show_image'),
    path('submit_guess/', m.submit_guess, name='submit_guess'),
]
