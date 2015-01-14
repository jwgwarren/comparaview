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
    
    return render_to_response('comparaview/omero_image.html',
         {'imageId':imageId,
         'image_name':image_name})
    
@login_required()
def full_viewer (request, iid, conn=None, **kwargs):
    """
    This view is responsible for showing the omero_image template
    Image rendering options in request are used in the display page. See L{getImgDetailsFromReq}.

    @param request:     http request.
    @param iid:         Image ID
    @param conn:        L{omero.gateway.BlitzGateway}
    @param **kwargs:    Can be used to specify the html 'template' for rendering
    @return:            html page of image and metadata
    """

    rid = getImgDetailsFromReq(request)
    try:
        image = conn.getObject("Image", iid)
        if image is None:
            logger.debug("(a)Image %s not found..." % (str(iid)))
            raise Http404
        d = {'blitzcon': conn,
             'image': image,
             'opts': rid,
             'build_year': build_year,
             'roiCount': image.getROICount(),
             'viewport_server': kwargs.get('viewport_server', reverse('webgateway')).rstrip('/'),# remove any trailing slash
             'object': 'image:%i' % int(iid)}

        template = kwargs.get('template', 'comparaview/omero_image.html')
        t = template_loader.get_template(template)
        c = Context(request,d)
        rsp = t.render(c)
    except omero.SecurityViolation:
        raise Http404
    return HttpResponse(rsp)

def getImgDetailsFromReq (request, as_string=False):
    """ Break the GET information from the request object into details on how to render the image.
    The following keys are recognized:
    z - Z axis position
    t - T axis position
    q - Quality set (0,0..1,0)
    m - Model (g for greyscale, c for color)
    p - Projection (see blitz_gateway.ImageWrapper.PROJECTIONS for keys)
    x - X position (for now based on top/left offset on the browser window)
    y - Y position (same as above)
    c - a comma separated list of channels to be rendered (start index 1)
      - format for each entry [-]ID[|wndst:wndend][#HEXCOLOR][,...]
    zm - the zoom setting (as a percentual value)

    @param request:     http request with keys above
    @param as_string:   If True, return a string representation of the rendering details
    @return:            A dict or String representation of rendering details above.
    @rtype:             Dict or String
    """

    r = request.REQUEST
    rv = {}
    for k in ('z', 't', 'q', 'm', 'zm', 'x', 'y', 'p'):
        if r.has_key(k):
           rv[k] = r[k]
    if r.has_key('c'):
        rv['c'] = []
        ci = _split_channel_info(r['c'])
        logger.debug(ci)
        for i in range(len(ci[0])):
            # a = abs channel, i = channel, s = window start, e = window end, c = color
          rv['c'].append({'a':abs(ci[0][i]), 'i':ci[0][i], 's':ci[1][i][0], 'e':ci[1][i][1], 'c':ci[2][i]})
    if as_string:
        return "&".join(["%s=%s" % (x[0], x[1]) for x in rv.items()])
    return rv