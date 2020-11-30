# -*- coding: utf-8 -*-
from rest_framework import serializers
from products.models.branding.Section import Section

class SectionSerializer(serializers.ModelSerializer):

	class Meta:

		model = Section
		fields = (

			'id',
			'name',
			'image',
			'createdAt',
			'updatedAt'
		)
