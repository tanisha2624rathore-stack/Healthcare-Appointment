from django.urls import path
from .import views

urlpatterns = [
    path('sign/',views.sign_up,name='sign'),
    path('login/',views.login,name='login'),
    path('view_doctor/',views.view_doctor,name='view_doctor'),
    path('book_app/',views.book_appointment,name='book_app'),
    path('show_app/',views.show_appointment,name='show_app'),
    path('get_slot/',views.get_booked_slots,name='get_slot'),
    path('symptom_view/',views.symptom_view,name='symptom_view')
]