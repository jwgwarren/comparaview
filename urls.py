from django.conf.urls import url, patterns
from omeroweb.comparaview import views

urlpatterns = patterns('django.views.generic.simple',

     # index 'home page' of the <your-app> app
     url( r'^$', views.index, name='comparaview_index' ),
     url( r'^stack_preview/(?P<imageId>[0-9]+)/$', views.stack_preview,
     name="<your-app>_stack_preview" ),

 )