# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models.sub_component_2.Table4 import Table4

class Table4Serializer(serializers.ModelSerializer):

	class Meta:

		model = Table4
		fields = (

			'id',
			'column1',
			'createdAt',
			'updatedAt'
		)
