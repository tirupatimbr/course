# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from . models import Topics,CourseCategory,User,Course,PaymentDetails
# from django.contrib.auth.hashers import make_password,check_password
# from rest_framework.authtoken.models import Token
# import json



# #**********************---------Payment----------*************************

#  stripe.api_key = 'sk_test_51InGpRSDVFjrWu4pHE4vNX10oAexpEJqzMRfVTrKmAG2HxvwbqkrmojLI14FgXcYYglLOm0DYzqiD51z5jTe24ql00UGLqxXAS'



# @api_view(['POST'])
# def payment_details(request):
# 	if request.method == 'POST':
# 		username = request.data.get('username')
# 		amount = request.data.get('amount')
# 		course_name = request.data.get('course_name')
# 		pay_date = request.data.get('pay_date')
# 		payment_id = request.data.get('payment_id')
# 		payment_status = request.data.get('payment_status')


# 		try:
# 			user_ins = User.objects.get(username=username)
# 		except:
# 			return JsonResponse({'success':True,'data':'admin or students not registered'})	

# 		try:
# 			course_ins= Course.objects.get(course_name=course_name)
# 		except:
# 			return JsonResponse({'success':False,'data':'data does not exist'})	
	




# 		payment_qs = stripe.PaymentIntent.create(user=user_ins,
# 												amount=amount,
# 												course=course_ins,
# 												pay_date=pay_date,
# 												payment_id=payment_id,
# 												payment_status=payment_status
# 												)
# 		return JsonResponse({'success':True,'data':payment_qs})







# # user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
# # 	amount = models.FloatField(null=True,blank=True)
# # 	course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
# # 	pay_date = models.DateField(null=True,blank=True)
# # 	payment_id = models.CharField(max_length=64,null=True,blank=True)
# # 	payment_status = models.BooleanField(null=True,blank=True)
   









# # @api_view(['POST'])
# # def test_payment(request):
# # test_payment_intent = stripe.PaymentIntent.create(
# #     amount=1000, currency='pln', 
# #     payment_method_types=['card'],
# #     receipt_email='test@example.com')
# # return Response(status=status.HTTP_200_OK, data=test_payment_intent)
