import datetime

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

# Create your models here.


INCIDENT_STATUS_CHOICES = (
		('open', 'Open'),
        ('closed', 'Closed'),
	)

RESPONDER_STATUS_CHOICES = (
	('pending', 'Pending'),
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
	
	def __unicode__(self):
	        return u'%s %s' % (self.incident.id, self.responder.username)
	

	
	
