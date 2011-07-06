import datetime

from piston.handler import BaseHandler
from callamedic.models import Incident
from piston.utils import rc
from callamedic.models import *
from callamedic.views import manage_incident

class IncidentHandler(BaseHandler):
	allowed_methods = ('GET','POST','PUT')
	
	model = Incident
	
	#Responder retrieves incident
	def read(self, request, incident_id=None, android_id=None):
		if incident_id:
			return Incident.objects.get(pk=incident_id)
		else:
			return 0
	
	#999 creates incident
	def create(self, request):
		data = request.data
		
		point = Point(float(data["lat"]),float(data["lon"]))
		incident = self.model(timestamp=datetime.datetime.now(), point=point, address=data.get("address", None), status= data.get("status", "open"))
		incident.save()
		#start incident response process here
		#manage_incident(incident) 
		
		response = rc.CREATED
		response.content = {"id":str(incident.id)}
		return response
	
	#999 updates with new info on incident	
	def update(self, request, incident_id=None):
		data = request.data
		
		incident = Incident.objects.get(id=incident_id)
		incident.status = data["status"]
		
		incident.save()
		
		return incident
		
class ResponderHandler(BaseHandler):
	allowed_methods = ('POST','PUT',)
	
	model = Responder
	
	#Responder Registration
	def create(self, request):
		data = request.data
		phone=Phone(android_id=data["android_id"])
		phone.save()
		responder = self.model(phone=phone, username=data["username"], first_name=data.get("firstname", None), last_name=data.get("lastname", None), email=data["email"], organization=data.get("organization", None) )
		responder.save()
		
		return responder
	
	#Responder login/logout
	def update(self, request, android_id = None):
		responder = Responder.objects.get(phone=android_id)
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
	
	#Responder sends in their location
	def create(self, request):
		data = request.data
		
		point = Point(float(data["lat"]),float(data["lon"]))
		responder_location = self.model(timestamp=datetime.datetime.now(), point=point)
		responder_location.responder = Responder.objects.get(phone=data["android_id"])
		responder_location.save()
		
		return responder_location
		
class IncidentResponderHandler(BaseHandler):
	allowed_methods = ('PUT',)
	
	#Responder updates their status on a response
	def update(self, request, incident_id = None, android_id = None):
		data = request.data
		
		response = "%s responders status on incident %s changed to %s" % (android_id, incident_id, data["status"])
		
		return response
			
		
		
		
		