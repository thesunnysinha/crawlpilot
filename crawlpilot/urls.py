from django.contrib import admin
from django.urls import path,include
from crawlpilotApp import urls as crawlpilotApp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(crawlpilotApp_urls))
]
