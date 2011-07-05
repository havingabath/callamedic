from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from callamedic.models import *
import time
import thread


#not finished
def alert_responders(incident):
	if incident.number_responding < 3:
		wave_ir = incident.get_standby_responders[:5]
		for ir in wave_ir:
			ir.tickle()
	time.sleep(30)
	
#not finished
def manage_incident(incident):
	incident_responders=incident.create_incident_responders()
	
		
	
	
def main_page(request):
	template = get_template('main_page.html')
	variables = Context({
		'head_title': u'CallamediC',
		'page_title':u'Welcome to Callamedic',
		'page_body':u'Saving your app one ass at a time!'
	})
	output = template.render(variables)
	return HttpResponse(output)
	

	
		