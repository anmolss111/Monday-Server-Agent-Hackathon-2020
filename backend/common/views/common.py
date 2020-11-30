# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.apps import apps

import random
import string
import os
import shutil

import json

def copytree(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

def get_settings_file(modules):

	text = """# -*- coding: utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5v)#089q5$+tampfwaxxixy%cw2*oz#-o1$n9vy8#aq@j!z%^u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [

	'django.contrib.contenttypes',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_extensions',
	'rest_framework',
	'corsheaders',
	'django_archive',
	'common',
"""

	for module in modules:

		text += '	\'' + module + '\',\n'

	text+= ']'

	text+= """

MIDDLEWARE = [

	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jarvis.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'jarvis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {

	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join('./main.db'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# CORS

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (

	'GET',
	'POST',
	'PATCH',
	'DELETE',
	'OPTIONS',
)

CORS_ALLOW_HEADERS = (

	'accept',
	'accept-encoding',
	'authorization',
	'content-type',
	'dnt',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
	'accesstoken',
	'request-from-type',
	'app-name'
)

ARCHIVE_FILENAME = 'Backup'

REST_FRAMEWORK = {

	'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
	'UNAUTHENTICATED_USER': None
}

ARCHIVE_EXCLUDE = ()

	"""

	return(text)

def get_urls_file(modules):

	text = """# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

"""
	for module in modules:

		text += '	url(r\'^' + module + '/\', include(\'' + module + '.urls\')),\n'

	text += """
]
"""

	return(text)

def get_apps_file(app):

	text = """# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class """ + app.title() + """Config(AppConfig):

	name = '""" + app + """'
	"""

	return(text)

def get_app_urls_file(module, components):

	text = """# -*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [

"""
	for component in components:

		text += """	url(r'^""" + component['name'] + """/', include('""" + module + """.routes.""" + component['name'] + """.urls')),\n"""

	text += """
]
	"""

	return(text)

def get_models_file(table, columns, modules, tableMap):

	text = """# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
"""

	for column in columns:

		if(column['type'] == 'Foreign'):

			for module in modules:

				for component in modules[module]:

					forgienKeyTableName = ''

					for tableEl in tableMap:

						if(tableMap[tableEl] == column['forgienKeyTable']):

							forgienKeyTableName = tableEl

					if(forgienKeyTableName in component['tables']):

						text += """from """ + module + """.models.""" + component['name'] + """.""" + forgienKeyTableName + """ import """ + forgienKeyTableName + """\n"""

	text +="""

class """ + table + """(models.Model):

	id = models.AutoField(primary_key=True)
"""

	for column in columns:

		text += """	""" + column['name'] + """ = models."""

		if(column['type'] == 'Char'):

			text += """CharField(max_length=255, blank=True, null=True)\n"""

		if(column['type'] == 'Text'):

			text += """TextField(blank=True, null=True)\n"""

		if(column['type'] == 'Foreign'):

			forgienKeyTableName = ''

			for table in tableMap:

				if(tableMap[table] == column['forgienKeyTable']):

					forgienKeyTableName = table

			text += 'ForeignKey(' + forgienKeyTableName + ', on_delete=models.CASCADE, blank=True, null=True)\n'

	text += """	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

"""

	for column in columns:

		text += """		if('""" + column['name'] + """' in data):\n"""

		if(column['type'] == 'Foreign'):

			forgienKeyTableName = ''

			for table in tableMap:

				if(tableMap[table] == column['forgienKeyTable']):

					forgienKeyTableName = table

			text += """			modelObject = """ + forgienKeyTableName + """.objects.filter(id=data['""" + column['name'] + """']).first()
"""
			text += """			self.""" + column['name'] + """ = modelObject\n
"""

		else:

			text += """			self.""" + column['name'] + """ = data['""" + column['name'] + """']\n
"""

	return(text)

def get_app_routes_urls_file(module, component, tables):

	text = """# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
"""

	for table in tables:

		text += """
import """ + module + """.views.""" + component + """.""" + table + """ as """ + table + """View"""

	text += """
urlpatterns = {

"""

	apis = []

	for table in tables:

		text += """	url(r'^""" + table.lower() + """/create$', """ + table + """View.create), \n"""
		text += """	url(r'^""" + table.lower() + """/read$', """ + table + """View.read), \n"""
		text += """	url(r'^""" + table.lower() + """/update$', """ + table + """View.update), \n"""
		text += """	url(r'^""" + table.lower() + """/delete$', """ + table + """View.delete), \n"""

		apis.append(module + '/' + component + '/' + table.lower() + '/create')
		apis.append(module + '/' + component + '/' + table.lower() + '/read')
		apis.append(module + '/' + component + '/' + table.lower() + '/update')
		apis.append(module + '/' + component + '/' + table.lower() + '/delete')

	text += """}

urlpatterns = format_suffix_patterns(urlpatterns)"""

	return (text,apis)

def get_serializers_file(module, component, table, columns):

	text = """# -*- coding: utf-8 -*-
from rest_framework import serializers
"""

	text += """from """ + module + """.models.""" + component + """.""" + table + """ import """ + table

	text +="""

class """ + table +"""Serializer(serializers.ModelSerializer):

	class Meta:

		model = """ + table + """
		fields = (

			'id',
"""

	for column in columns:

		text += """			'""" + column['name'] + """',\n"""

	text += """			'createdAt',
			'updatedAt'
		)
"""

	return (text)


def get_views_files(module, component, table):

	text = """# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.apps import apps
from common.services.common import get, post, patch, delete

import json
"""

	text += """from """ + module + """.models.""" + component + """.""" + table + """ import """ + table

	text += """

@api_view(['POST'])
def create(request, format=None):

	response = post(request, """ + table + """)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def read(request, format=None):

	response = get(request, """ + table + """)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def update(request, format=None):

	response = patch(request, """ + table + """)

	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)

@api_view(['POST'])
def delete(request, format=None):

	response = delete(request, """ + table + """)
	return Response({

		'status': 'success',
		'data': response
	},status=status.HTTP_200_OK)
"""

	return (text)

def getMakeMigrationsFile(modules):

	text = ''

	for module in modules:

		text += 'python3 manage.py makemigrations ' + module + '\n'

	text += 'python3 manage.py migrate'

	return (text)

def getStartFile(modules):

	text = ''

	text += 'python3 manage.py runserver'

	return (text)

def get_random_string(length):

	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

@api_view(['POST'])
def service(request, format=None):

	requestBody = json.loads(request.body.decode('utf-8'))
	print(requestBody)

	cwd = os.path.abspath(os.getcwd())

	tempDirectory = cwd + '/temp/' + get_random_string(20)

	if not os.path.exists(tempDirectory):

		os.makedirs(tempDirectory)

	tempDirectory = tempDirectory + '/'

	shutil.copyfile(cwd + '/files/manage.py', tempDirectory + 'manage.py')
	shutil.copyfile(cwd + '/files/setup.sh', tempDirectory + 'setup.sh')

	os.chmod(tempDirectory + 'setup.sh' , 0o777)

	modulesMap = requestBody['modulesMap']
	tableRender = requestBody['tableRender']

	modules = {}
	for moduleMap in modulesMap:

		transformed = '_'.join(moduleMap.lower().split())
		modules[transformed] = []

		print(modulesMap[moduleMap])

		for component in modulesMap[moduleMap]:

			transformedComponent = '_'.join(component['name'].lower().split())

			tables = []
			if(component['tables'] != ''):

				tables = ''.join(component['tables'].split()).split(',')

			modules[transformed].append({

				'name': transformedComponent,
				'tables': tables
			})

	tableMap = {}
	for tableRenderIndex in range(0, len(tableRender)):

		tableRenderEl = tableRender[tableRenderIndex]
		table = ''.join(tableRenderEl['name'].split())
		tableMap[table] = tableRenderIndex

	tempDirectoryJarvis = tempDirectory + 'jarvis/'

	if not os.path.exists(tempDirectoryJarvis):

		os.makedirs(tempDirectoryJarvis)

	f = open(tempDirectoryJarvis + 'settings.py',"w+")
	f.write(get_settings_file(modules))
	f.close()

	f = open(tempDirectoryJarvis + 'urls.py',"w+")
	f.write(get_urls_file(modules))
	f.close()

	shutil.copyfile(cwd + '/files/wsgi.py', tempDirectoryJarvis + 'wsgi.py')

	if not os.path.exists(tempDirectory + 'common'):

		os.makedirs(tempDirectory + 'common')

	copytree(cwd + '/files/common', tempDirectory + 'common')

	f = open(tempDirectory + 'mirgrations.sh',"w+")
	f.write(getMakeMigrationsFile(modules))
	f.close()

	os.chmod(tempDirectory + 'mirgrations.sh' , 0o777)

	f = open(tempDirectory + 'start.sh',"w+")
	f.write(getStartFile(modules))
	f.close()

	os.chmod(tempDirectory + 'start.sh' , 0o777)

	apis = []

	for module in modules:

		appDirectory = tempDirectory + module + '/'

		if not os.path.exists(appDirectory):

			os.makedirs(appDirectory)

		f = open(appDirectory + 'apps.py',"w+")
		f.write(get_apps_file(module))
		f.close()

		f = open(appDirectory + 'urls.py',"w+")
		f.write(get_app_urls_file(module, modules[module]))
		f.close()

		appModelsDirectory = tempDirectory + module + '/models/'

		if not os.path.exists(appModelsDirectory):

			os.makedirs(appModelsDirectory)

		appRoutesDirectory = tempDirectory + module + '/routes/'

		if not os.path.exists(appRoutesDirectory):

			os.makedirs(appRoutesDirectory)

		appSerializersDirectory = tempDirectory + module + '/serializers/'

		if not os.path.exists(appSerializersDirectory):

			os.makedirs(appSerializersDirectory)

		appViewsDirectory = tempDirectory + module + '/views/'

		if not os.path.exists(appViewsDirectory):

			os.makedirs(appViewsDirectory)

		for component in modules[module]:

			appModelsComponentDirectory = appModelsDirectory + component['name'] + '/'

			if not os.path.exists(appModelsComponentDirectory):

				os.makedirs(appModelsComponentDirectory)

			print(component)

			for table in component['tables']:

				f = open(appModelsComponentDirectory + table + '.py',"w+")
				f.write(get_models_file(table , tableRender[tableMap[table]]['columns'], modules, tableMap))
				f.close()

			appRoutesComponentDirectory = appRoutesDirectory + component['name'] + '/'

			if not os.path.exists(appRoutesComponentDirectory):

				os.makedirs(appRoutesComponentDirectory)

			f = open(appRoutesComponentDirectory + 'urls.py',"w+")
			text, routesApis = get_app_routes_urls_file(module, component['name'], component['tables'])
			apis += routesApis
			f.write(text)
			f.close()

			appSerializersComponentDirectory = appSerializersDirectory + component['name'] + '/'

			if not os.path.exists(appSerializersComponentDirectory):

				os.makedirs(appSerializersComponentDirectory)

			for table in component['tables']:

				f = open(appSerializersComponentDirectory + table + '.py',"w+")
				f.write(get_serializers_file(module, component['name'] , table, tableRender[tableMap[table]]['columns']))
				f.close()

			appViewsComponentDirectory = appViewsDirectory + component['name'] + '/'

			if not os.path.exists(appViewsComponentDirectory):

				os.makedirs(appViewsComponentDirectory)

			for table in component['tables']:

				f = open(appViewsComponentDirectory + table + '.py',"w+")
				f.write(get_views_files(module, component['name'] , table))
				f.close()

	f = open(tempDirectory + 'apis.txt',"w+")
	f.write('\n'.join(apis))
	f.close()

	buildFile = 'Build-' + get_random_string(10)

	shutil.make_archive(buildFile, 'zip', tempDirectory)

	shutil.copyfile(cwd + '/' + buildFile + '.zip', cwd + '/static/' + buildFile + '.zip')

	return Response({

		'status': 'success',
		'build': buildFile + '.zip'
	},status=status.HTTP_200_OK)
