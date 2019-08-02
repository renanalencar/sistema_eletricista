from .development import *

ALLOWED_HOSTS = ['*']

DEBUG = True

DATABASES = {
	'default' : {
		'ENGINE' : 'django.db.backends.mysql',
		'NAME' : 'eletricista24hs',
		'USER' : 'eletricista24hs',
		'PASSWORD' : 'NSWFpj17',
		'HOST' : '',
		'POST' : '',
	}
}

STATICFILE_DIRS = (
	'/home/polijr/webapps/eletricista24hs_static/',
)

STATIC_ROOT = '/home/polijr/webapps/eletricista24hs_static/'


