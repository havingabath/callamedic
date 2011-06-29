from piston.handler import BaseHandler
from callamedic.models import Incident

class IncidentHandler(BaseHandler):
	allowed_methods = ('GET','POST',)
	
	def read(self, request, id=None):
		if id:
			return Incident.objects.get(pk=id)
		else:
			return 0
			
	def create(self, request):
			return '999 created an Incident'