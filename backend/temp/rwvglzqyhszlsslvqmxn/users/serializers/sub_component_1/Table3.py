# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models.sub_component_1.Table3 import Table3

class Table3Serializer(serializers.ModelSerializer):

	class Meta:

		model = Table3
		fields = (

			'id',
			'column1',
			'column2',
			'createdAt',
			'updatedAt'
		)
