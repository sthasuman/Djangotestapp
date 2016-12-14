"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from userlogin.views import MessageView, InboxView, NoticeView, CreateNoticeView, CreateBlogView, BlogView, BlogpostView,NotificationView




urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^view/$',"userlogin.views.index"),
    url(r'^register/$', "userlogin.views.register"), # ADD NEW PATTERN!
    url(r'^login/$', "userlogin.views.user_login"),
    url(r'^logout/$', "userlogin.views.user_logout"),
    url(r'^update/(?P<pk>[\d]+)$', "userlogin.views.update"),
    url(r'^delete/(?P<pk>[\d]+)$', "userlogin.views.delete"),
    url(r'^message/(?P<pk>[\d]+)$', MessageView.as_view()),
    url(r'^inbox/(?P<pk>[\d]+)$', InboxView.as_view()),
    url(r'^notice/$', NoticeView.as_view()),
    url(r'^addnotice/$', CreateNoticeView.as_view()),
    url(r'^addblog/(?P<pk>[\d]+)$', CreateBlogView.as_view()),
    url(r'^blog/$', BlogView.as_view()),
    url(r'^blogpost/(?P<pk>[\d]+)$', BlogpostView.as_view()),
    url(r'^notification/(?P<pk>[\d]+)$', NotificationView.as_view()),
    url(r'^$', "userlogin.views.index"),

]

