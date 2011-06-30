from piston.handler import BaseHandler
from callamedic.models import Incident

class IncidentHandler(BaseHandler):
	allowed_methods = ('GET','POST','PUT')
	
	def read(self, request, id=None, android_id=None):
		if id:
			return Incident.objects.get(pk=id)
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
	
	def create(self, request):
		data = request.data
		return "user with the following details has been created: %s" % data
	
	def update(self, request, android_id = None):
		data = request.data
		
		if data["on_call"] == "True":
			response = "%s is logged in" % android_id
		elif data["on_call"] == "False":
			response = "%s is logged out" % android_id
		else:
			response = 0
		
		return response
		
class ResponderLocationHandler(BaseHandler):
	allowed_methods = ('POST',)
	
	def create(self, request):
		data = request.data
		
		response = "%s is at location %s , %s" % (data["android_id"],data["lat"],data["lon"])
		
		return response
		
class IncidentResponderHandler(BaseHandler):
	allowed_methods = ('PUT',)
	
	def update(self, request, incident_id = None, android_id = None):
		data = request.data
		
		response = "%s responders status on incident %s changed to %s" % (android_id, incident_id, data["status"])
		
		return response
			
		
		
		
		