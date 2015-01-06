from django.conf.urls.defaults import *
from omeroweb.comparaview import views

urlpatterns = patterns('django.views.generic.simple',

     # index 'home page' of the <your-app> app
     url( r'^$', views.index, name='comparaview_index' ),

 )