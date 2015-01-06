from django.http import HttpResponse
from omeroweb.webclient.decorators import login_required
from django.shortcuts import render_to_response

def index(request):
    """
    Just a place-holder while we get started
    """
    return HttpResponse("Welcome to your app home-page2!")

@login_required()
def compare (request, imageId, conn=None, **kwargs):
    """ Shows a subset of Z-planes for an image """
    image = conn.getObject("Image", imageId)       # Get Image from OMERO
    image_name = image.getName()
    sizeZ = image.getSizeZ()                        # get the Z size
    # 5 Z-planes
    z_indexes = [0, int(sizeZ*0.25),
             int(sizeZ*0.5), int(sizeZ*0.75), sizeZ-1]
    return render_to_response('webtest/compare.html',
         {'imageId':imageId,
         'image_name':image_name,
         'z_indexes':z_indexes})