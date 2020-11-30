import json

from django.apps import apps
from django.core import serializers

def get(request, Model):

	requestBody = json.loads(request.body.decode('utf-8'))
	modelObjects = Model.objects

	for operation in requestBody:

		if(operation == 'filter'):

			for key in requestBody[operation]:

				if(key != 'filters'):

					if(not 'filters' in requestBody['filter']):

						kwargsFormat = 'in'

					else:

						kwargsFormat = requestBody['filter']['filters'][key]

					if(kwargsFormat != 'not_null_empty'):

						kwargs = {
							'{0}__{1}'.format(key, kwargsFormat): requestBody['filter'][key]
						}
						modelObjects = modelObjects.filter(**kwargs)

			for key in requestBody[operation]:

				if(key != 'filters'):

					if('filters' in requestBody['filter']):

						kwargsFormat = requestBody['filter']['filters'][key]

						if(kwargsFormat == 'not_null_empty'):

							kwargs = {
								'{0}__{1}'.format(key, 'isnull'): True
							}
							modelObjects = modelObjects.exclude(**kwargs)

		if(operation == 'all'):

			modelObjects = modelObjects.all()

	orderFlag = False

	for operation in requestBody:

		if(operation == 'orderBy'):

			orderFlag = True

	if(orderFlag == False):

		modelObjects = modelObjects.order_by('id')

	else:

		for column in requestBody['orderBy']:

			modelObjects = modelObjects.order_by(column)

	return serializers.serialize('python', modelObjects)

def post(request, Model):

	requestBody = json.loads(request.body.decode('utf-8'))
	modelObjects = Model.objects

	for operation in requestBody:

		if(operation == 'register'):

			for key in requestBody['register']['existingCheckColumns']:

				kwargs = {
					'{0}__{1}'.format(key, 'in'): [requestBody['register']['data'][key]]
				}
				modelObjects = modelObjects.filter(**kwargs)

	modelObjects = modelObjects.order_by('id')

	if(modelObjects.count() == 0 or requestBody['register']['existingCheckColumns'] == []):

		modelObjects = Model.objects.values('id').order_by('-id').first()

		model = Model(
			id=modelObjects['id']+1
		)
		model.save()

		model.jsonToClass(requestBody['register']['data'])
		model.save()

	else:

		model = modelObjects.first()

		model.jsonToClass(requestBody['register']['data'])
		model.save()

	modelObjects = Model.objects.filter(id=model.id)

	return serializers.serialize('python', modelObjects)

def patch(request, Model):

	requestBody = json.loads(request.body.decode('utf-8'))
	modelObjects = Model.objects

	modelObjects = modelObjects.filter(id=requestBody['update']['id'])

	if(modelObjects.count() != 0):

		model = modelObjects.first()

		model.jsonToClass(requestBody['update']['data'])
		model.save()

	return serializers.serialize('python', modelObjects)

def delete(request, modelName):

	print(1)
