from django.test import TestCase
from django.test import Client

# Create your tests here.
c = Client()
response = c.post('/v1/api/user/register/',{'username':'Markez','password':'drichlet_2014','mobile_number':'0716357527'})
print(response)
