from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from . models import Topics,CourseCategory,User,Course,PaymentDetails,ForgetPassword,UserCourse
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.authtoken.models import Token
import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from instamojo_wrapper import Instamojo
import random 
from django.db.models import Q

from django.utils import timezone
import datetime 
from datetime import datetime
from datetime import date
from django.core.mail import send_mail

import os
from twilio.rest import Client

@api_view(['POST'])
def user_register(request):
	if request.method == 'POST':
		username = request.data.get('username')
		password = request.data.get('password')
		email = request.data.get('email')
		ph_no = request.data.get('ph_no')
		user_type = request.data.get('user_type')

		if User.objects.filter(username=username).exists():
			return JsonResponse({'success':False,'data':'username already exists'})

		User.objects.create(username=username,
							password=make_password(password),
							email=email,
							ph_no=ph_no,
							user_type=user_type)

		return JsonResponse({'success':True,'data':'user data posted'})


def authenticate(username=None,password=None):
	user = User.objects.get(username=username)
	print(user,'aaaaaaaaaaaaa') 

	return user.check_password(password)


@api_view(['GET'])
def login_user(request):
	if request.method == 'GET':
		username = request.data.get('username')
		password = request.data.get('password')

		try:
			user_ins = User.objects.get(username=username)
		except:
			return JsonResponse({'success':False,'data':'user not registered'})    

		user = authenticate(username=username,password=password)
		print(user,'uuuuuuuuuu')

		if user:
			try:
				token = Token.objects.get(user_id = user_ins.id)
				print(token,'ttttttttttttttt')
				
			except:
				token = Token.objects.create(user_id = user_ins.id)

			user_qs = list(User.objects.filter(username=username).values())
			return JsonResponse({'success':True,'data':user_qs,'token':token.key})  

		else:
			return JsonResponse({'success':False,'data':'wrong password'})

				

@api_view(['PUT'])
def user_update(request):
	if request.method == 'PUT':
		user_id = request.data.get('user_id')
		username = request.data.get('username')
		password = request.data.get('password')
		email = request.data.get('email')
		ph_no = request.data.get('ph_no')
		user_type = request.data.get('user_type')

		if User.objects.filter(username=username).exists():
			return JsonResponse({'success':False,'data':'username already exists'})

		if user_id:
			if User.objects.filter(id=user_id).exists():
				User.objects.filter(id=user_id).update(username=username,
														password=make_password(password),
														email=email,
														ph_no=ph_no,
														user_type=user_type)
				return JsonResponse({'success':True,'data':'user data updated'})
			return JsonResponse({'success':False,'data':'given wrong user_id '})
		return JsonResponse({'success':False,'data':'your user_id not mention'})
			





@api_view(['DELETE'])
def user_delete(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})
	

	elif request.method == 'DELETE' and request.user.user_type == 'admin':
		user_id = request.data.get('user_id')

		if user_id:
			if User.objects.filter(id=user_id).exists():
				User.objects.filter(id=user_id).delete()
				return JsonResponse({'success':True,'data':'user deleted'})
			return JsonResponse({'success':False,'data':'given wrong user_id '})
		return JsonResponse({'success':False,'data':'your user_id not mention'})
	return JsonResponse({'success':False,'data':'only admin can delete '})


@api_view(['GET'])
def userdetails(request):
	if request.method == 'GET':
		qs = list(User.objects.all().values())
		return JsonResponse({'success':True,'data':qs})




#*************************************CATEGORY************************************************************# 


@api_view(['POST'])
def add_categories(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})
	

	elif request.method == 'POST' and request.user.user_type == 'admin':
		category_name = request.data.get('category_name')

		if CourseCategory.objects.filter(category_name=category_name).exists():
			return JsonResponse({'success':False,'data':'category_name already exists'})

		CourseCategory.objects.create(category_name=category_name)
		return JsonResponse({'success':True,'data':'Added course category'})
	return JsonResponse({'success':False,'data':'only admin can add '})


@api_view(['PUT'])
def update_categories(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'PUT' and request.user.user_type == 'admin':
		category_name = request.data.get('category_name')
		category_id = request.data.get('category_id')

		if CourseCategory.objects.filter(category_name=category_name).exists():
				return JsonResponse({'success':False,'data':'category_name already exists'})

		if category_id:
				
			if CourseCategory.objects.filter(id=category_id).exists():

				CourseCategory.objects.filter(id=category_id).update(category_name=category_name)
				return JsonResponse({'success':True,'data':'updated course category'})
			return JsonResponse({'success':False,'data':'given wrong category_id '})
		return JsonResponse({'success':False,'data':'your category_id not mention'})

	return JsonResponse({'success':False,'data':'only admin can add '})


@api_view(['DELETE'])
def delete_categories(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'DELETE' and request.user.user_type == 'admin':
		category_id = request.data.get('category_id')

		if category_id:
			if CourseCategory.objects.filter(id=category_id).exists():
				CourseCategory.objects.filter(id=category_id).delete()
				return JsonResponse({'success':True,'data':'CourseCategory deleted'})
			return JsonResponse({'success':False,'data':'given wrong category_id '})
		return JsonResponse({'success':False,'data':'your category_id not mention'})
		
					
	return JsonResponse({'success':False,'data':'only admin can delete '})
	





@api_view(['GET'])
def category_details(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'GET' and request.user.user_type == 'admin':
		category_id = request.GET.get('category_id')

		if category_id:
			category_ins = list(CourseCategory.objects.filter(id=category_id).values())
			return JsonResponse({'success':True,'data':category_ins})

		category_qs = list(CourseCategory.objects.all().values())
		return JsonResponse({'success':True,'data':category_qs})
	return JsonResponse({'success':False,'data':'only admin can retrive details '})
		



#*************************---------TOPICS---------****************************************      





@api_view(['POST'])
def add_topics(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'POST' and request.user.user_type == 'admin':
		topic_name = request.data.get('topic_name')

		if Topics.objects.filter(topic_name=topic_name).exists():
			return JsonResponse({'success':False,'data':'topic_name already exists'})   
		

		Topics.objects.create(topic_name=topic_name)
		return JsonResponse({'success':False,'data':'topic_name created'})
	return JsonResponse({'success':False,'data':'only admin can add details'})  
		

@api_view(['PUT'])
def update_topics(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'PUT' and request.user.user_type == 'admin':
		topic_id = request.data.get('topic_id') 
		topic_name = request.data.get('topic_name')

		if topic_id:
			if Topics.objects.filter(id=topic_id).exists():
				Topics.objects.filter(id=topic_id).update(topic_name=topic_name)
				return JsonResponse({'success':True,'data':'topic_name updated'})   
			return JsonResponse({'success':False,'data':'topic_id given wrong'})    
		return JsonResponse({'success':False,'data':'topic_id not mention'})    
	return JsonResponse({'success':False,'data':'only admin can update details'})   
		

@api_view(['DELETE'])
def delete_topics(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'DELETE' and request.user.user_type == 'admin':
		topic_id = request.data.get('topic_id') 

		if topic_id:
			if Topics.objects.filter(id=topic_id).exists():
				Topics.objects.filter(id=topic_id).delete()
				return JsonResponse({'success':True,'data':'topic_name deleted succesfully'})
			return JsonResponse({'success':False,'data':'topic_id given wrong'})    
		return JsonResponse({'success':False,'data':'topic_id not mention'})    
	return JsonResponse({'success':False,'data':'only admin can update details'})   
		

@api_view(['GET'])
def topic_details(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'GET' and request.user.user_type == 'admin':
		topic_id = request.GET.get('topic_id')

		if topic_id:
			topic_qs = list(Topics.objects.filter(id=topic_id).values())
			return JsonResponse({'success':True,'data':topic_qs})
		topic_qs = list(Topics.objects.all().values())
		return JsonResponse({'success':True,'data':topic_qs})
	return JsonResponse({'success':False,'data':'only admin can retrive details'})  
	


#********************-------COURSE-------********************************



@api_view(['POST'])
def add_coursedetails(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token'})

	elif request.method == 'POST' and request.user.user_type == 'admin':
		course_name = request.data.get('course_name')
		created_by = request.data.get('created_by')
		available_date = request.data.get('available_date')
		description = request.data.get('description')
		actual_price = request.data.get('actual_price')
		offer_price = request.data.get('offer_price')
		logo = request.data.get('logo')
		created_date = request.data.get('created_date')
		course_link = request.data.get('course_link')
		enable = request.data.get('enable')

		category_id = request.data.get('category_id')
		topics_lt = request.data.get('topics_lt')


		if Course.objects.filter(course_name=course_name).exists():
			return JsonResponse({'success':False,'data':'course_name already exists'})  

		try:
			category_ins = CourseCategory.objects.get(id=category_id)
			print(category_ins.id,type(category_ins),'ccccccccccc')
		except:
			return JsonResponse({'success':False,'data':'category_id does not exists'})


		try:
			course_ins = Course.objects.get(course_name=course_name)
		except:
			course_ins = Course.objects.create(course_name=course_name,
							course_category=category_ins,
							created_by=request.user,
							available_date=available_date,
							description=description,
							actual_price=actual_price,
							offer_price=offer_price,
							logo=logo,
							created_date=created_date,
							course_link=course_link,
							enable=enable)
		


		topic_data = json.loads(topics_lt)
		print(topic_data,'dddddddddd')
		print(type(topic_data),'tttttttttttt')
		for i in topic_data:
			print(i,'iiiiiiiiii')
			try:
				topic_ins = Topics.objects.get(id=i)
			except:
				return JsonResponse({'success':False,'data':'valid topics_id are selectd remaining not exist'})


			course_ins.topics.add(topic_ins)    
						
		return JsonResponse({'success':True,'data':'course data added succesfully'})    

	return JsonResponse({'success':False,'data':'only admin can add details'})  


@api_view(['PUT'])
def update_coursedetails(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token autharization'})

	elif request.method == 'PUT' and request.user.user_type == 'admin':
		course_id = request.data.get('course_id')
		course_name = request.data.get('course_name')
		created_by = request.data.get('created_by')
		available_date = request.data.get('available_date')
		description = request.data.get('description')
		actual_price = request.data.get('actual_price')
		offer_price = request.data.get('offer_price')
		logo = request.data.get('logo')
		created_date = request.data.get('created_date')
		course_link = request.data.get('course_link')
		enable = request.data.get('enable')

		category_id = request.data.get('category_id')
		topics_lt = request.data.get('topics_lt')


		if Course.objects.filter(course_name=course_name).exists():
			return JsonResponse({'success':False,'data':'course_name already exists'})  

		try:
			category_ins = CourseCategory.objects.get(id=category_id)
			print(category_ins.id,type(category_ins),'ccccccccccc')
		except:
			return JsonResponse({'success':False,'data':'category_id does not exists'})


		try:
			course_ins = Course.objects.get(id=course_id)
		except:
			return JsonResponse({'success':False,'data':'course_id does not exists'})


		if logo:
			course_ins.logo=logo
		course_ins.save()       

		course_ins.topics.clear()

		try:
			topic_data = json.loads(topics_lt)
			for i in topic_data:
				try:
					topic_ins = Topics.objects.get(id=i)
				except:
					return JsonResponse({'success':False,'data':'some topics_id are selectd remaining not exist'})
		
				course_ins.topics.add(topic_ins)    
		except:
			return JsonResponse({'success':False,'data':'topics_id does not exist'})
		
				
		Course.objects.filter(id=course_id).update(course_name=course_name,
													course_category=category_ins,
													created_by=request.user,
													available_date=available_date,
													description=description,
													actual_price=actual_price,
													offer_price=offer_price,
													created_date=created_date,
													course_link=course_link,
													enable=enable)

		return JsonResponse({'success':True,'data':'course data updated succesfully'})  

	return JsonResponse({'success':False,'data':'only admin can update details'})   


@api_view(['DELETE'])
def delete_course(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token autharization'})

	elif request.method == 'DELETE' and request.user.user_type == 'admin':
		course_id = request.data.get('course_id')

		if course_id:
			if Course.objects.filter(id=course_id).exists():
				Course.objects.filter(id=course_id).delete()
				return JsonResponse({'success':True,'data':'course deleted succesfully'})
			return JsonResponse({'success':True,'data':'course id given wrong'})    
		return JsonResponse({'success':True,'data':'course id does not mention'})
	return JsonResponse({'success':False,'data':'only admin can delete course details'})    



@api_view(['GET'])
def course_details(request):
	if request.user.is_anonymous:
		return JsonResponse({'success':False,'data':'you have to give token autharization'})

	elif request.method == 'GET' and request.user.user_type == 'admin':
		course_id = request.GET.get('course_id')

		if course_id:
			course_qs = list(Course.objects.filter(id=course_id).values())
			# return JsonResponse({'success':True,'data':course_qs})



		course_qs = list(Course.objects.all().values()) 

		course_lt = []
		for course in course_qs:
			category_qs = list(CourseCategory.objects.filter(id=course['course_category_id']).values())
			user_qs = list(User.objects.filter(id=course['created_by_id']).values('username'))
						
			
		
			for catg in category_qs:
				catg_dic={}
				catg_dic['category_name'] = catg['category_name']
				# print(catg_dic)
		
			for user in user_qs:
				user_dic={}             
				user_dic['username'] = user['username']
			# print(user_dic)   
			
			try:
				course_ins= Course.objects.get(id=course["id"])
			except:
				return JsonResponse({'success':False,'data':'data does not exist'}) 


			course_dict ={}
			course_dict['topic_name'] = list(course_ins.topics.values())
			course_dict['course_name'] = course['course_name']
			course_dict['course_link'] = course['course_link']
			course_dict['logo'] = course['logo']
			course_dict['created_date'] = course['created_date']
			course_dict['actual_price'] = course['actual_price']
			course_dict['offer_price'] = course['offer_price']
			course_dict['available_date'] = course['available_date']
			course_dict['enable'] = course['enable']
			course_dict['description'] = course['description']
			course_dict['category_name'] = catg_dic['category_name']
			course_dict['user'] = user_dic['username']

			course_lt.append(course_dict)


			# topics = list(Topics.objects.all().values())
			# print(topics,'tttttttttttttt')

		return JsonResponse({'success':True,'data':course_lt})
	return JsonResponse({'success':False,'data':'only admin can retrive course details'})   
	


#***********************---------PORTAL-------********************************




@api_view(['GET'])
def portal(request):
	if request.method == 'GET':
		course_qs=list(Course.objects.filter(enable=True).values())
		return JsonResponse({'success':True,'data':course_qs})


#*********************************************************************************
from django.conf import settings
import random

@api_view(['POST'])
def payment_start(request):
	if request.method == 'POST':
		amount = request.data.get("amount")
		purpose = request.data.get("purpose")
		# email = request.data.get('email')
		# phone = request.data.get('phone')
		# buyer_name = request.data.get('buyer_name')
		order_id = request.data.get('order_id')
		user_id = request.data.get('user_id')
		course_id = request.data.get('course_id')
		

		api = Instamojo(api_key='test_f577794476b1ef07f7575c9cd62',
				auth_token='test_6f3d4b2cf04d758cd46685ce523',
				endpoint = 'https://test.instamojo.com/api/1.1/')

		
		response = api.payment_request_create(amount=amount,
											  purpose='Course',
											
											  # send_email = True,
											  # send_sms = True,
											  # email=email,
											  # phone=phone,
											  # buyer_name=buyer_name,
											  redirect_url="http://www.google.com/")

		
		try:
			user_instance = User.objects.get(id=user_id)
		except:
			return JsonResponse({'success':False,'data':'user does not exist'})

		try:
			course_instance = Course.objects.get(id=course_id)
		except:
			return JsonResponse({'success':False,'data':'course id does not exist'})
	

	
	
		random_num = random.randint(11111,99999)
		print(random_num,'rrrrrrrrrr')
		order_id = "{}{}".format(request.user.id,random_num)
		print(order_id,'ooooooooooooooooo')


		PaymentDetails.objects.create(order_id= order_id,   #response['payment_request']['id']
										amount = amount,
										payment_status = 'pending',
										user_id = user_instance.id,
										course = course_instance)

										

		return JsonResponse({'success':True,'order_id':order_id,'data':response})

#************************************************

@api_view(['PUT'])
def store_payments_details(request):
	if request.method == 'PUT':
		order_id = request.data.get('order_id')
		payment_id = request.data.get('payment_id')
		payment_status = request.data.get('payment_status')
		pay_date = request.data.get('pay_date')

		if payment_status == 'Credit':
			PaymentDetails.objects.filter(order_id=order_id).update(payment_id=payment_id,
																	payment_status='Credit',
																	pay_date = pay_date
																	)
			try:
				ins=PaymentDetails.objects.get(order_id=order_id)
				print(ins.user,'user')
				print(ins.course,'course')
			except:
				return JsonResponse({'success':True,'data':'order id does not exist'})

			try:
				qs = UserCourse.objects.get(user=ins.user)	
				print(qs,'get')	
			except:
				qs = UserCourse.objects.create(user=ins.user)	
				print(qs,'create')	

			qs.course.add(ins.course)	
					

			return JsonResponse({'success':True,'data':'store_payments succesfully'})


		else:
			PaymentDetails.objects.filter(order_id=order_id).update(payment_id=payment_id,
																	payment_status='failed',
																	pay_date = pay_date
																	)
			return JsonResponse({'success':True,'data':'store_payments failed'})


#*******************************************************************

# @api_view(['PUT'])
# def store_payments_details(request):
# 	if request.method == 'PUT':
# 		order_id = request.data.get('order_id')
# 		payment_id = request.data.get('payment_id')
# 		payment_status = request.data.get('payment_status')
# 		pay_date = request.data.get('pay_date')
		
		
# 		PaymentDetails.objects.filter(order_id=order_id).update(payment_id=payment_id,
# 																payment_status=payment_status,
# 																pay_date = pay_date
# 																)

																												
# 		return JsonResponse({'success':True,'data':'store_payments_details'})


#******************
	







@api_view(['GET'])
def status_payment(request):
	if request.method == 'GET':
		payment_request_id = request.data.get('payment_request_id')


		api = Instamojo(api_key='test_f577794476b1ef07f7575c9cd62',
				auth_token='test_6f3d4b2cf04d758cd46685ce523',
				endpoint = 'https://test.instamojo.com/api/1.1/')


		response = api.payment_request_status(payment_request_id)

		print(response['payment_request']['shorturl'],'shorturl')  # Get the short URL
		print(response['payment_request']['status'],'status')   # Get the current status
		print(response['payment_request']['payments'],'payments')  # List of payments


		return JsonResponse({'success':True,'data':response})


		


@api_view(['GET'])
def Payment_related_Payment_Request(request):
	if request.method == 'GET':
		payment_request_id = request.data.get('payment_request_id')
		payment_id = request.data.get('payment_id')



		api = Instamojo(api_key='test_f577794476b1ef07f7575c9cd62',
				auth_token='test_6f3d4b2cf04d758cd46685ce523',
				endpoint = 'https://test.instamojo.com/api/1.1/')

		

		response = api.payment_request_payment_status(payment_request_id,payment_id)

		return JsonResponse({'success':True,'data':response})



@api_view(['GET'])
def list_of_payment_requests(request):
	if request.method == 'GET':

		api = Instamojo(api_key='test_f577794476b1ef07f7575c9cd62',
				auth_token='test_6f3d4b2cf04d758cd46685ce523',
				endpoint = 'https://test.instamojo.com/api/1.1/')

		response = api.payment_requests_list()
		return JsonResponse({'success':True,'data':response})

#*******************************************************************************************************



@api_view(['GET'])
def list_of_courses(request):
	if request.method == 'GET':

		course_qs = list(Course.objects.all().values('id','course_name'))
		li=[]
		for course in course_qs:
			count =  PaymentDetails.objects.filter(course_id=course['id'],payment_status='Credit').count()
			if count > 0:
				course["count"] = count
				li.append(course)
		return JsonResponse({'success':True,'data':li})


# @api_view(['GET'])
# def user_of_courses(request):
#   if request.method == 'GET':

#       course_qs=list(Course.objects.all().values())
#       print(course_qs,'llllllllllllll')

#       course_li=[]
#       for course in course_qs:
#           qs = list(PaymentDetails.objects.filter(course_id=course['id'],payment_status='Credit').values())
#           dic = {}
#           dic['course_name'] = course['course_name']
#           # dic['count'] =  len(qs)
#           if len(qs)>0:                   ###
#               dic['count'] =  len(qs)     #### 

			
#               course_li.append(dic)

	
				
#       return JsonResponse({'success':True,'data':course_li})





# @api_view(['GET'])
# def user_of_courses(request):
#   if request.method == 'GET':

#       course_qs=list(Course.objects.all().values())


#       li=[]
#       for course in course_qs:
#           qs = list(PaymentDetails.objects.filter(course_id=course['id'],payment_status='Credit').values())
#           dic = {}
#           dic['course_name'] = course['course_name']
#           dic['count'] = len(qs)
#           lst = []
#           for user in qs:
#               user_ins = User.objects.get(id = user['user_id']).username
#               lst.append(user_ins)

#           dic['users'] = lst

#           print(qs)
#           print('\n')
#           li.append(dic)
				
#       return JsonResponse({'success':True,'data':li})



@api_view(['GET'])
def user_of_courses(request):
	if request.method == 'GET':

		course_qs=list(Course.objects.all().values())

		li=[]
		for course in course_qs:
			qs = list(PaymentDetails.objects.filter(course_id=course['id'],payment_status='Credit').values())
			dic = {}
			dic['course_name'] = course['course_name']
			dic['count'] = len(qs)
			lst = []
			for user in qs:
				dt={}
				user_ins = User.objects.get(id = user['user_id'])
				dt['username'] = user_ins.username
				dt['ph_no'] = user_ins.ph_no

				lst.append(dt)

			dic['users'] = lst

			print(qs)
			print('\n')
			li.append(dic)
				
		return JsonResponse({'success':True,'data':li})




#******************************************************************************************************


@api_view(['GET'])
def course_expiry(request):
  if request.user.is_anonymous:
	  return JsonResponse({'Success':False,'data':'you have to give token autharization'})

  elif request.method == 'GET':
	  course_id = request.data.get('course_id')
	  try:
		  course_ins = Course.objects.get(id=course_id)
		  if date.today() <= course_ins.expiry:
			  qs = PaymentDetails.objects.filter(course=course_ins,user=request.user,payment_status='Credit')
			  if qs:
				  return JsonResponse({'success':True,'data':list(qs.values())})
			  else:
				  return JsonResponse({'success':False,'data':'can not access for course because not purchase'})
		  else:
			  return JsonResponse({'success':False,'data':'course expiry'})

	  except:
		  return JsonResponse({'success':False,'data':'course  does not exist'})

# @api_view(['GET'])
# def course_expiry(request):
#   if request.user.is_anonymous:
#       return JsonResponse({'Success':False,'data':'you have to give token autharization'})

#   elif request.method == 'GET':
#       course_id = request.data.get('course_id')

#       try:
#           course_ins = Course.objects.get(id=course_id)

#           if Course.objects.filter(id=course_ins.id,expiry__gte=datetime.today()).exists():
#               qs = PaymentDetails.objects.filter(course=course_ins,user=request.user,payment_status='Credit')
#               if qs:
#                   return JsonResponse({'success':True,'data':list(qs.values())})
#               else:
#                   return JsonResponse({'success':False,'data':'can not access for course because not purchase'})
#           else:
#               return JsonResponse({'success':False,'data':'course expiry'})
					
#       except:
#           return JsonResponse({'success':True,'data':'course_id does not exist'}) 
				
		



#*****************************************************************************************************


@api_view(['GET'])
def total_payment(request):
	if request.user.is_anonymous:
		return JsonResponse({'Success':False,'data':'you have to give token autharization'})

	elif request.method == 'GET' and request.user.user_type == 'admin':
		course_id = request.GET.get('course_id')
		print(course_id)
		li=[]
		if course_id:
			try:
				course_ins = Course.objects.get(id=course_id)

				qs = list(PaymentDetails.objects.filter(course=course_ins,payment_status='Credit').values())

				s=0
				dic={}
				for i in qs:
					s=s+i['amount']
				dic['total_amount'] = s
				dic['course_name'] = course_ins.course_name
				li.append(dic)
				return JsonResponse({'success':True,'data':li})

			except:
				return JsonResponse({'success':True,'data':'course does not exist'})
						
		else:
			qs = list(PaymentDetails.objects.filter(payment_status='Credit').values())
			
			s=0
			dic={}
			for i in qs:
				s=s+i['amount']
			dic['total_amount'] = s
			li.append(dic)
			return JsonResponse({'success':True,'data':li}) 

				
	return JsonResponse({'success':False,'data':'only admin can access course payment details'})    


#*******************************************************************************************            
import datetime

@api_view(['GET'])
def user_course_expiry_email(request):
	if request.user.is_anonymous:
		return JsonResponse({'Success':False,'data':'you have to give token autharization'})

	elif request.method == 'GET':
		print(request.user)
		print(request.user.email)

		qs = list(PaymentDetails.objects.filter(user=request.user,payment_status='Credit').values())
		print(qs)

		if qs:
			courses =' '
			for course in qs:
				course_ins = Course.objects.get(id=course['course_id'])
				print(course_ins)

				diff = course_ins.expiry - date.today()
				print(diff.days)
			
				if 0< diff.days <= 5:
					c_name = course_ins.course_name
					days = diff.days
					courses = courses + ' ' + c_name

					subject = "Alert"
					message = "you {} course expiry with in 5  days" .format(courses)
					to = request.user.email
				  
				

				else:
					pass

			send_mail(subject,message,'tirupatimbr@gmail.com',[to],fail_silently=False)

			return JsonResponse({'success':True,'data':'Mail Sent < 5 days (or) other wise not sending'})
		else:
			return JsonResponse({'success':False,'data':'can not access for course because not purchase'})  

#********************************************************************************************
import os
from twilio.rest import Client

@api_view(['GET'])
def user_course_expiry_message(request):
	if request.user.is_anonymous:
		return JsonResponse({'Success':False,'data':'you have to give token autharization'})

	elif request.method == 'GET':
		print(request.user)
		print(request.user.email)
		print(request.user.ph_no)

		qs = list(PaymentDetails.objects.filter(user=request.user,payment_status='Credit').values())
		print(qs)

		if qs:
			courses =' '
			for course in qs:
				course_ins = Course.objects.get(id=course['course_id'])
				print(course_ins)

				diff = course_ins.expiry - date.today()
				print(diff.days)
			
				if 0< diff.days <= 5:
					c_name = course_ins.course_name
					days = diff.days
					phone_no = request.user.ph_no
					print(request.user.ph_no,'phone')

					courses = courses + ' ' + c_name

					account_sid = 'AC72bf07f8a4ff608668bcf510adebdd52'
					auth_token = '301fa4ad8c096cd745e1d21b21339c97'
					client = Client(account_sid, auth_token)

					# message = client.messages.create(
		   #                            body= "you {} kkk course expiry with in 5  days" .format(courses),
		   #                            from_='+13177933278',
		   #                            to = '+91'+str(phone_no))

					# print(message.sid)


				else:
					pass

			message = client.messages.create(
									  body= "your {} course expiry with in 5  days" .format(courses),
									  from_='+13177933278',
									  to = '+91'+str(phone_no))

			print(message.sid)      

			return JsonResponse({'success':True,'data':'sms Sent < 5 days (or) other wise not sending'})

		else:
			return JsonResponse({'success':False,'data':'can not access for course because not purchase'})  




#*******************************************************************

#FkOv9Y_KwdeKawDcztWMKWhRN7NblDFpEQS1SD9A

# AC72bf07f8a4ff608668bcf510adebdd52 act sid
# 301fa4ad8c096cd745e1d21b21339c97 token
# (317) 793-3278
# +13177933278


@api_view(['GET'])
def text_message(request):
	if request.method == 'GET':


		account_sid = 'AC72bf07f8a4ff608668bcf510adebdd52'
		auth_token = '301fa4ad8c096cd745e1d21b21339c97'
		client = Client(account_sid, auth_token)

		message = client.messages.create(
									  body='This is text message from python',
									  from_='+13177933278',
									  to='+919491678078'
								  )

		print(message.sid)

		return JsonResponse({'success':True,'data':'sms send succesfully'})




# import os
# from twilio.rest import Client
# import random

# @api_view(['GET'])
# def text_message(request):
#   if request.method == 'GET':

#       otp = random.randint(1000,9999)
#       print(otp)
#       print(request.user)


#       account_sid = 'AC72bf07f8a4ff608668bcf510adebdd52'
#       auth_token = '301fa4ad8c096cd745e1d21b21339c97'
#       client = Client(account_sid, auth_token)

#       message = client.messages.create(
#                                     body='This is text message from python :'+str(otp),
#                                     from_='+13177933278',
#                                     to='+919491678078'
#                                 )

#       print(message.sid)

#       return JsonResponse({'success':True,'data':'sms send succesfully'})


#*************************************************************************************************************

@api_view(['GET'])
def forgot_password(request):
	if request.method == 'GET':
		otp = random.randint(1000,9999)
		print(otp)
		# print(request.user.username,'tttt')
		phone_no = request.user.ph_no
		
		# account_sid = 'AC72bf07f8a4ff608668bcf510adebdd52'
		# auth_token = '301fa4ad8c096cd745e1d21b21339c97'
		# client = Client(account_sid, auth_token)

		# message = client.messages.create(
		# 							  body='This is text message from python :'+str(otp),
		# 							  from_='+13177933278',
		# 							  to='+91'+str(phone_no)
		# 							  )
		# print(message.sid)

		try:
			user_ins = User.objects.get(id=request.user.id)
			print(user_ins,'uuuuuuuuuuu')
		except:
			return JsonResponse({'sucess':True,'data':'user does not exist'})


		try:
			data = ForgetPassword.objects.get(user=user_ins)
			print(data,'get')
			data.otp = otp
			data.save() 
		except:
			otp_ins = ForgetPassword.objects.create(otp=otp,user=user_ins)
			print(otp_ins,'create')				
		return JsonResponse({'sucess':True,'data':'otp send succesfully'})	
	return JsonResponse({'sucess':True,'data':'invalid'})


@api_view(['POST'])
def reset_password(request):
	if request.method=='POST':
		otp = request.data.get('otp')
		password = request.data.get('password')

		print(otp,'otp')
		print(request.user)

		qs = list(ForgetPassword.objects.filter(user=request.user.id,otp=otp).values())
		print(qs,'oooooooooo')
		if qs:
			User.objects.filter(id=request.user.id).update(password=make_password(password))
			return JsonResponse({'sucess':True,'data':'password change succesfully'})
	
		return JsonResponse({'sucess':True,'data':'user token not Authorized'})	

	return JsonResponse({'sucess':True,'data':'password '})























#**************************************************


# http://www.example.com/handle_redirect.py?
# payment_id=MOJO1505D05A04390572&
# payment_status=Credit&
# payment_request_id=d2d0e1287f95476c80ff812bd2b5c789


# http://www.example.com/handle_redirect.py?
# payment_id=MOJO1505X05A04390582&
# payment_status=Credit&
# payment_request_id=1fa2646e0c534304bfa77e0611be05eb


# https://test.instamojo.com/order/status/9a717457-2bcc-49a6-829c-da6dc4966dbb/?
# token=1491254738208b170032bd64f1e6bf824fb67b24e7583dc6b21b45211776ea1f8834d74662ac7
# 5f0003d28c9f6c7991d965c0e0a34754151dbeed8a266af0f51


# http://www.example.com/handle_redirect.py?
# payment_id=MOJO1505005A04390588&
# payment_status=Failed&
# payment_request_id=9ec6f5d49cc74f56a4f9b3441569add4

#20/05/2021
# https://www.google.com/?
# payment_id=MOJO1520905A79297979&
# payment_status=Credit&
# payment_request_id=4d84a2362f8a457d9b35d33c0db21c6b





# {
#     "success": true,
#     "data": {
#         "success": true,
#         "payment_request": {
#             "redirect_url": "http://www.google.com/",
#             "send_sms": true,
#             "shorturl": null,
#             "amount": "12.00",
#             "buyer_name": null,
#             "webhook": null,
#             "phone": "+919491678078",
#             "longurl": "https://test.instamojo.com/@tirupatipalem/6998c561971b4d3e933581e4d7ca6e00",
#             "purpose": "Course",
#             "modified_at": "2021-05-05T06:09:03.334840Z",
#             "status": "Pending",
#             "id": "6998c561971b4d3e933581e4d7ca6e00",
#             "expires_at": null,
#             "email": "tirupatipalem@gmail.com",
#             "allow_repeated_payments": true,
#             "email_status": "Pending",
#             "customer_id": null,
#             "created_at": "2021-05-05T06:09:03.334818Z",
#             "sms_status": "Pending",
#             "send_email": true
#         }
#     }
# }




# {
#     "success": true,
#     "data": {
#         "success": true,
#         "payment_request": {
#             "sms_status": null,
#             "id": "d2d0e1287f95476c80ff812bd2b5c789",
#             "modified_at": "2021-05-05T05:20:25.620457Z",
#             "created_at": "2021-05-05T05:17:12.505944Z",
#             "expires_at": null,
#             "status": "Completed",
#             "purpose": "Course",
#             "amount": "5500.00",
#             "send_sms": false,
#             "send_email": false,
#             "phone": null,
#             "redirect_url": "http://www.example.com/handle_redirect.py",
#             "customer_id": null,
#             "longurl": "https://test.instamojo.com/@tirupatipalem/d2d0e1287f95476c80ff812bd2b5c789",
#             "buyer_name": null,
#             "payments": [
#                 {
#                     "affiliate_commission": "0",
#                     "instrument_type": "CARD",
#                     "buyer_name": "ttt",
#                     "amount": "5500.00",
#                     "shipping_state": null,
#                     "shipping_zip": null,
#                     "shipping_country": null,
#                     "variants": [],
#                     "shipping_city": null,
#                     "payment_id": "MOJO1505D05A04390572",
#                     "shipping_address": null,
#                     "failure": null,
#                     "quantity": 1,
#                     "tax_invoice_id": "",
#                     "payout": null,
#                     "status": "Credit",
#                     "payment_request": "https://test.instamojo.com/api/1.1/payment-requests/d2d0e1287f95476c80ff812bd2b5c789/",
#                     "buyer_email": "tirupatipalem@gmail.com",
#                     "currency": "INR",
#                     "billing_instrument": "International Regular Credit Card (Visa/Mastercard)",
#                     "fees": "104.50",
#                     "buyer_phone": "9491678078",
#                     "custom_fields": {},
#                     "created_at": "2021-05-05T05:19:33.400390Z",
#                     "unit_price": "5500.00"
#                 }
#             ],
#             "allow_repeated_payments": true,
#             "email_status": null,
#             "email": null,
#             "shorturl": null,
#             "webhook": null
#         }
#     }
# }


# {
#     "data": {
#         "payment_request": {
#             "shorturl": null,
#             "id": "d2d0e1287f95476c80ff812bd2b5c789",
#             "webhook": null,
#             "amount": "5500.00",
#             "send_sms": false,
#             "phone": null,
#             "email": null,
#             "email_status": null,
#             "modified_at": "2021-05-05T05:20:25.620457Z",
#             "expires_at": null,
#             "sms_status": null,
#             "buyer_name": null,
#             "longurl": "https://test.instamojo.com/@tirupatipalem/d2d0e1287f95476c80ff812bd2b5c789",
#             "allow_repeated_payments": true,
#             "created_at": "2021-05-05T05:17:12.505944Z",
#             "purpose": "Course",
#             "status": "Completed",
#             "payment": {
#                 "tax_invoice_id": "",
#                 "payout": null,
#                 "affiliate_commission": "0",
#                 "shipping_address": null,
#                 "payment_request": "https://test.instamojo.com/api/1.1/payment-requests/d2d0e1287f95476c80ff812bd2b5c789/",
#                 "created_at": "2021-05-05T05:19:33.400390Z",
#                 "billing_instrument": "International Regular Credit Card (Visa/Mastercard)",
#                 "currency": "INR",
#                 "custom_fields": {},
#                 "buyer_email": "tirupatipalem@gmail.com",
#                 "payment_id": "MOJO1505D05A04390572",
#                 "fees": "104.50",
#                 "shipping_zip": null,
#                 "quantity": 1,
#                 "buyer_phone": "9491678078",
#                 "amount": "5500.00",
#                 "unit_price": "5500.00",
#                 "variants": [],
#                 "shipping_city": null,
#                 "failure": null,
#                 "buyer_name": "ttt",
#                 "shipping_state": null,
#                 "status": "Credit",
#                 "shipping_country": null,
#                 "instrument_type": "CARD"
#             },
#             "redirect_url": "http://www.example.com/handle_redirect.py",
#             "customer_id": null,
#             "send_email": false
#         },
#         "success": true
#     },
#     "success": true
# }




@api_view(['GET'])
def complex_query(request):
	if request.method == 'GET':
		course_id = request.GET.get('course_id')
		if course_id:
			qs = list(Course.objects.filter(id=course_id).values())
			return JsonResponse({'success':True,'data':qs})


		# qs = list(Course.objects.filter(
		#   Q(course_name__startswith='j') | Q(course_name__endswith='s')).values('course_name')) 


		# qs = list(Course.objects.filter(
		#   Q(course_name__startswith='j') & Q(course_name__endswith='a')).values('course_name'))

		# qs = list(Course.objects.filter(
		#   Q(course_name__startswith='j') | Q(course_name__startswith='s')).values('course_name'))

		qs = list(Course.objects.filter(
			Q(course_name__startswith='java') &  Q(description__endswith='g')).values())

		# qs = list(Course.objects.filter(
		#   Q(course_name__startswith='java') & Q(description__startswith='ga')).values('course_name'))
		return JsonResponse({'success':True,'data':qs})





