from django.urls import path
from courseapp import views





urlpatterns = [
    path('user_register/', views.user_register),
    path('login_user/',views.login_user),
    path('user_update/',views.user_update),
    path('user_delete/',views.user_delete),
    path('userdetails/',views.userdetails),

    path('add_categories/',views.add_categories),
    path('update_categories/',views.update_categories),
    path('delete_categories/',views.delete_categories),
    path('category_details/',views.category_details),

    path('add_topics/',views.add_topics),
    path('update_topics/',views.update_topics),
    path('delete_topics/',views.delete_topics),
    path('topic_details/',views.topic_details),

    path('add_coursedetails/',views.add_coursedetails),
    path('update_coursedetails/',views.update_coursedetails),
    path('delete_course/',views.delete_course),
    path('course_details/',views.course_details),

    path('portal/',views.portal),
    
    path('payment_start/',views.payment_start),
    path('store_payments_details/',views.store_payments_details),


    path('status_payment/',views.status_payment),
    path('Payment_related_Payment_Request/',views.Payment_related_Payment_Request),
    path('list_of_payment_requests/',views.list_of_payment_requests),
    
    path('complex_query/',views.complex_query),
   
    path('list_of_courses/',views.list_of_courses),
    path('user_of_courses/',views.user_of_courses),

    path('course_expiry/',views.course_expiry),
    path('total_payment/',views.total_payment),
    path('user_course_expiry_email/',views.user_course_expiry_email),
    path('user_course_expiry_message/',views.user_course_expiry_message),
    path('text_message/',views.text_message),

    path('forgot_password/',views.forgot_password),
    path('reset_password/',views.reset_password),
]



