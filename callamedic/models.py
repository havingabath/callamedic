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
		

class Location(models.Model):
	geometry = models.PointField()  #srid = 4326   - EPSG number
	timestamp = models.DateTimeField()

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
	
	
