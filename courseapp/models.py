from django.db import models

from django.contrib.auth.models import AbstractUser

class Topics(models.Model):
	topic_name = models.CharField(max_length=64,null=True,blank=True)

	def __str__(self):
		return self.topic_name


class CourseCategory(models.Model):
	category_name = models.CharField(max_length=64,null=True,blank=True)

	def __str__(self):
		return self.category_name

class User(AbstractUser):
	ph_no = models.CharField(max_length=64,null=True,blank=True)
	user_type = models.CharField(max_length=64,null=True,blank=True)


class Course(models.Model):
	course_category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE,null=True,blank=True)
	topics = models.ManyToManyField(Topics,blank=True)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	course_name = models.CharField(max_length=64,null=True,blank=True)
	available_date = models.DateField(null=True,blank=True)
	description = models.TextField(null=True,blank=True) 
	actual_price = models.FloatField(null=True,blank=True)
	offer_price = models.FloatField(null=True,blank=True)
	logo = models.ImageField(upload_to='images',null=True,blank=True)
	created_date = models.DateField(null=True,blank=True)
	course_link = models.URLField(max_length=64,null=True,blank=True)
	enable = models.BooleanField(null=True,blank=True)
	expiry = models.DateField(null=True,blank=True)

	def __str__(self):
		return self.course_name


class PaymentDetails(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	amount = models.FloatField(null=True,blank=True)
	course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
	pay_date = models.DateField(null=True,blank=True)
	payment_id = models.CharField(max_length=64,null=True,blank=True)
	payment_status = models.CharField(max_length=64,null=True,blank=True)
	order_id = models.CharField(max_length=64,null=True,blank=True)

	# def __str__(self):
	# 	return self.payment_status



class ForgetPassword(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    otp = models.CharField(max_length=20,null=True,blank=True)
    
  

class UserCourse(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	course = models.ManyToManyField(Course)


