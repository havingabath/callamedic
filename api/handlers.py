import datetime

from piston.handler import BaseHandler
from callamedic.models import Incident
from piston.utils import rc
from callamedic.models import *

class IncidentHandler(BaseHandler):
	allowed_methods = ('GET','POST','PUT')
	
	def read(self, request, incident_id=None, android_id=None):
		if incident_id:
			return Incident.objects.get(pk=incident_id)
		else:
			return 0
		
	def create(self, request):
		data = request.data
		return data
		
	def update(self, request, id=None):
		data = request.data
		
		if data["status"] == "closed":
			return "Incident %s is closed" % id
		elif data["status"] == "open":
			return "Incident %s is open" % id
		else:
			return 0
		
class ResponderHandler(BaseHandler):
	allowed_methods = ('POST','PUT',)
	
	model = Responder
	
	def create(self, request):
		data = request.data
		responder = self.model(android_id=data["android_id"], username=data["username"], first_name=data.get("firstname", None), last_name=data.get("lastname", None), email=data["email"], organization=data.get("organization", None) )
		responder.save()
		return responder
	
	def update(self, request, android_id = None):
		responder = Responder.objects.get(android_id=android_id)
		data = request.data
		if data["on_call"] == "True":
			responder.on_call = True
		elif data["on_call"] == "False":
			responder.on_call = False
		
		responder.save()
		
		return responder
		
class ResponderLocationHandler(BaseHandler):
	allowed_methods = ('POST',)
	
	model = ResponderLocation
	
	def create(self, request):
		data = request.data
		
		geometry = Point(float(data["lat"]),float(data["lon"]))
		responder_location = self.model(timestamp=datetime.datetime.now(), geometry=geometry)
		responder_location.responder = Responder.objects.get(android_id=data["android_id"])
		responder_location.save()
		
		return responder_location
		
class IncidentResponderHandler(BaseHandler):
	allowed_methods = ('PUT',)
	
	def update(self, request, incident_id = None, android_id = None):
		data = request.data
		
		response = "%s responders status on incident %s changed to %s" % (android_id, incident_id, data["status"])
		
		return response
			
		
		
		
		