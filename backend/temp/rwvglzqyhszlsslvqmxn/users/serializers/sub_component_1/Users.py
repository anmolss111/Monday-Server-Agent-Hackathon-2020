# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models.sub_component_1.Users import Users

class UsersSerializer(serializers.ModelSerializer):

	class Meta:

		model = Users
		fields = (

			'id',
			'firstName',
			'lastName',
			'emailAddress',
			'password',
			'createdAt',
			'updatedAt'
		)
