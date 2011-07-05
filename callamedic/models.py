import datetime, time

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

# Create your models here.


INCIDENT_STATUS_CHOICES = (
		('open', 'Open'),
        ('closed', 'Closed'),
	)

RESPONDER_STATUS_CHOICES = (
	('standby', 'Standby'),
	('tickled', 'Tickled'),
	('recieved', 'Recieved'),
	('rejected', 'Rejected'),
	('en_route', 'En_route'),
	('cancelled', 'Cancelled'),
	('at_scene', 'At_scene'),
	('finished', 'Finished'),	
)

class Phone(models.Model):
	android_id = models.CharField(primary_key=True, max_length=16)
	device_id = models.CharField(unique=True, max_length=255, null=True)
	
	
class Responder(User):
	phone = models.OneToOneField(Phone, primary_key=True)
	organization = models.TextField(blank=True)
	on_call = models.BooleanField(default=False)
	cert_valid_to = models.DateTimeField(null=True)
	verified = models.BooleanField(default=False)
	
	def get_most_recent_location(self):
		location = None
        #get all responders locations and sort by time, then return most recent
		loc_set = ResponderLocation.objects.filter(responder=self).order_by('-timestamp')
		if len(loc_set) > 0:
			location = loc_set[0]
		return location
		

class Location(models.Model):
	point = models.PointField()  #srid = 4326   - EPSG number
	timestamp = models.DateTimeField()
	address = models.CharField(max_length=300, null=True)

	objects = models.GeoManager()

	class Meta:
		abstract = True


class Incident(Location):
	status = models.CharField(max_length=6, choices=INCIDENT_STATUS_CHOICES)
	responders = models.ManyToManyField(Responder, through='IncidentResponder')

	def __unicode__(self):
		return u'%s %s' % (self.id, self.timestamp)
	
	#not finished	
	def create_incident_responders(self):
		""""on_call_responders = Responder.objects.filter(on_call=True)
		on_call_locations = []
		
		for r in on_call_responders:
			on_call_locations.append(r.get_most_recent_location)
		
		eligible_locations = on_call_locations.filter(point__distance_lte=(self.point,D(km=10))).distance(self.point).order_by('distance')
		eligible_responders = []
		
		for l in eligible_locations:
			eligible_responders.append(l.responder)"""
		#rls = ResponderLocation.objects.filter(point__distance_lte=(self.point,D(km=10))).distance(self.point).order_by('distance')
		responders = Responder.objects.all()[:5]     #dummy return
		incident_responders = []
		for r in responders:
			ir = IncidentResponder(responder=r,incident=self,status='standby')
			ir.save()
			incident_responders.append(ir)
		return incident_responders
		
	def number_responding(self):
		incident_responders = IncidentResponder.objects.filter(incident=self)
		x = 0
		for ir in incident_responders:
			if ir.is_responding():
				x+=1
		return x
		
	def number_on_standby(self):
		return IncidentResponder.objects.filter(incident=self, status='standby').count()
		
	def get_standby_responders(self):
		return IncidentResponder.objects.filter(incident=self, status='standby')
		
		
		
		

class ResponderLocation(Location):
	responder = models.ForeignKey(Responder)

	def __unicode__(self):
		return u'%s %s' % (self.responder.username, self.timestamp)

	
class IncidentResponder(models.Model):
	responder = models.ForeignKey(Responder)
	incident = models.ForeignKey(Incident)
	status = models.CharField(max_length=10, choices=RESPONDER_STATUS_CHOICES)
	contacted_at = models.DateTimeField(null=True)
	# include other important times to capture in this class
	
	class Meta:
		unique_together = ['responder', 'incident']
	
	def __unicode__(self):
	        return u'%s %s' % (self.incident.id, self.responder.username)
	
	def tickle(self):
		#C2DM stuff here
		self.status = "tickled"
		self.contacted_at = datetime.datetime.now()
		self.save()
		
	def is_responding(self):
		return self.status == "en_route" or self.status == "at_scene"
		
	

	
	
