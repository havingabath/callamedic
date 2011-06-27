from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def main_page(request):
	template = get_template('main_page.html')
	variables = Context({
		'head_title': u'CallamediC',
		'page_title':u'Welcome to Callamedic',
		'page_body':u'Saving your app one ass at a time!'
	})
	output = template.render(variables)
	return HttpResponse(output)
		