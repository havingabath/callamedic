import datetime

from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.


INCIDENT_STATUS_CHOICES = (
		('open', 'Open'),
        ('closed', 'Closed'),
	)

RESPONDER_STATUS_CHOICES = (
	('alerted', 'Alerted'),
	('pending', 'Pending'),
	('rejected', 'Rejected'),
	('en_route', 'En_route'),
	('cancelled', 'Cancelled'),
	('at_scene', 'At_scene'),	
)

	
class Responder(User):
	organization = models.TextField(blank=True)
	android_id = models.IntegerField(unique=True)
	on_call = models.BooleanField(default=False)
	certificate_valid_to = models.DateTimeField()
		
class Incident(models.Model):
	status = models.CharField(max_length=6, choices=INCIDENT_STATUS_CHOICES)
	responders = models.ManyToManyField(Responder, through='IncidentResponder')
	
	def __unicode__(self):
	        return u"%i" % self.id
	
class ResponderLocation(models.Model):
	geometry = models.PointField()  #srid = 4326   - EPSG number
	timestamp = models.DateTimeField()
	responder = models.ForeignKey(Responder)

	objects = models.GeoManager()
	
	def __unicode__(self):
	        return u'%s %s' % (self.responder.username, self.timestamp)

class IncidentLocation(models.Model):
	geometry = models.PointField()  #srid = 4326   - EPSG number
	timestamp = models.DateTimeField()
	incident = models.ForeignKey(Incident)
	#need to include field(s) to save address
	
	objects = models.GeoManager()
	
	def __unicode__(self):
	        return u'%s %s' % (self.incident.id, self.timestamp)
	
class IncidentResponder(models.Model):
	responder = models.ForeignKey(Responder)
	incident = models.ForeignKey(Incident)
	status = models.CharField(max_length=10, choices=RESPONDER_STATUS_CHOICES)
	contacted_at = models.DateTimeField(null=True)
	# include other important times to capture in this class
	
	def __unicode__(self):
	        return u'%s %s' % (self.incident.id, self.responder.username)
	
	
