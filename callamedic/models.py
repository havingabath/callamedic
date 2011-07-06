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
	
		
	def create_incident_responders(self):
		eligible_locations = ResponderLocation.objects.filter(responder__on_call=True,latest=True).filter(point__distance_lte=(self.point,D(km=10))).distance(self.point).order_by('distance')
		incident_responders = []
		for el in eligible_locations:
			ir = IncidentResponder(responder=el.responder,incident=self,status='standby')
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
	latest = models.BooleanField() # dirty solution

	def __unicode__(self):
		return u'%s %s' % (self.responder.username, self.timestamp)
		
	#ensures there is only ever one latest location per Responder
	def save(self, *args, **kwargs):
		previous_latest_location = ResponderLocation.objects.filter(responder=self.responder, latest=True)
		if previous_latest_location:
			previous_latest_location.update(latest=False)
		self.latest = True
		super(ResponderLocation, self).save(*args, **kwargs)


	
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
		
	

	
	
