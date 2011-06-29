from django.conf.urls.defaults import *
from piston.resource import Resource
from medic.api.handlers import IncidentHandler

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

incident_handler = CsrfExemptResource(IncidentHandler)

urlpatterns = patterns('',
    url(r'^incident/(?P<id>[^/]+)/', incident_handler),
	url(r'^incident/', incident_handler),
)