from django.conf.urls.defaults import *
from piston.resource import Resource
from medic.api.handlers import IncidentHandler, ResponderHandler, ResponderLocationHandler, IncidentResponderHandler

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

incident_handler = CsrfExemptResource(IncidentHandler)
responder_handler = CsrfExemptResource(ResponderHandler)
responderlocation_handler = CsrfExemptResource(ResponderLocationHandler)
incidentresponder_handler = CsrfExemptResource(IncidentResponderHandler)



urlpatterns = patterns('',
    url(r'^incident/(?P<id>[^/]+)/(?P<android_id>[^/]+)/', incident_handler),
	url(r'^incident/$', incident_handler),
	url(r'^responder/(?P<android_id>[^/]+)/', responder_handler),
	url(r'^responder/$', responder_handler),
	url(r'^responder_location/$', responderlocation_handler),
	url(r'^incident_responder/(?P<incident_id>[^/]+)/(?P<android_id>[^/]+)/', incidentresponder_handler),
)