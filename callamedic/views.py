from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from callamedic.models import *
import time
import threading

#this loop will repeat at set intervals
def repeat(event_timer, incident_id, interval, alert):
	while True:
		incident = Incident.objects.get(id=incident_id)
		if incident.status == "closed" or event_timer.isSet():
			break
		alert(incident)
		event_timer.wait(interval)

#this checks the number of repsonders responding, and if not enough, alerts more standby responders
def alert_more_responders(incident):
	if incident.number_responding < 3:
		wave_of_incident_responders = incident.get_standby_responders[:5]
		for ir in wave_of_incident_responders:
			ir.tickle()
	
#this manages an incident
def manage_incident(incident):
	#create incident Responders
	incident.create_incident_responders()
	#set up event and thread
	event_timer = threading.Event()
	#the function alert responders will be called with asscoiated arguments
	incident_thread = threading.Thread(target=repeat, args=(event_timer, incident.id, 30.0, alert_more_responders))
	#start_incident thread
	incident_thread.start()
	#leave run for 15 minutes
	time.sleep(60*15)
	#then set it so it stops
	event_timer.set()
	incident_thread.join() 
	
		
def main_page(request):
	template = get_template('main_page.html')
	variables = Context({
		'head_title': u'CallamediC',
		'page_title':u'Welcome to Callamedic',
		'page_body':u'Saving your app one ass at a time!'
	})
	output = template.render(variables)
	return HttpResponse(output)
	

	
		