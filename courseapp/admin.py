from django.contrib import admin

from . models import Topics,CourseCategory,User,Course,PaymentDetails,ForgetPassword,UserCourse

class TopicsAdmin(admin.ModelAdmin):
	list_display = ['id','topic_name']

class CourseCategoryAdmin(admin.ModelAdmin):
	list_display = ['id','category_name']

class UserAdmin(admin.ModelAdmin):
	list_display = ['id','username','password','email','ph_no','user_type']

class CourseAdmin(admin.ModelAdmin):
	list_display = ['id','course_name','course_category','created_by','available_date',
								'description','actual_price','offer_price','logo',
								'created_date','course_link','enable','expiry']

class PaymentDetailsAdmin(admin.ModelAdmin):
	list_display = ['id','user','amount','course','pay_date','payment_id','payment_status','order_id']	

class ForgetPasswordAdmin(admin.ModelAdmin):
	list_display = ['id','user','otp']	

class UserCourseAdmin(admin.ModelAdmin):
	list_display = ['id','user']										

admin.site.register(Topics,TopicsAdmin)
admin.site.register(CourseCategory,CourseCategoryAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(PaymentDetails,PaymentDetailsAdmin)	
admin.site.register(ForgetPassword,ForgetPasswordAdmin)
admin.site.register(UserCourse,UserCourseAdmin)