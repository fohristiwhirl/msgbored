from django.conf.urls import url

import views

urlpatterns = [
    url(r"^msg$", views.msg_submit, name="msg_submit"),
    url(r"^destroy$", views.destroy_all, name="destroy_all"),
    url(r"^$", views.form, name="form"),
]
