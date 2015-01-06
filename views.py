from omeroweb.webclient.decorators import login_required
from django.shortcuts import render_to_response


@login_required()
def stack_preview (request, imageId, conn=None, **kwargs):
    """ Shows a subset of Z-planes for an image """
    image = conn.getObject("Image", imageId)       # Get Image from OMERO
    image_name = image.getName()
    sizeZ = image.getSizeZ()                        # get the Z size
    # 5 Z-planes
    z_indexes = [0, int(sizeZ*0.25),
             int(sizeZ*0.5), int(sizeZ*0.75), sizeZ-1]
    return render_to_response('webtest/stack_preview.html',
         {'imageId':imageId,
         'image_name':image_name,
         'z_indexes':z_indexes})