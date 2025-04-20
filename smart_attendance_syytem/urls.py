"""
URL configuration for smart_attendance_syytem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views,Hod_views,staff_views,student_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='name'),

    #login path
    path('',views.LOGIN,name='login'),
    path('dologin',views.dologin,name="dologin"),
    path('dologout',views.dologout,name="logout"),

    #profile update
    path('profile',views.PROFILE,name='profile'),
    path('profile/update',views.PROFILE_UPDATE,name="profile_update"),
    
    # this is hod url
    path('hod/home', Hod_views.HOME, name='hod_home'),
    path('hod/Student/Add', Hod_views.ADD_STUDENT, name="add_student"),
    path('hod/Student/View', Hod_views.VIEW_STUDENT, name="view_student"),
    path('hod/Student/Edit/<str:id>', Hod_views.EDIT_STUDENT, name="edit_student"),
    path('hod/Student/Update', Hod_views.UPDATE_STUDENT, name="update_student"),
    # path('hod/Student/Delete/<str:admin>', Hod_views.DELETE_STUDENT, name="delete_student"),
    path('hod/Student/Delete/<int:admin>/', Hod_views.DELETE_STUDENT, name='delete_student'),
    path('hod/Student/Leave_view', Hod_views.STUDENT_LEAVE_VIEW, name="student_leave_view"),
    path('hod/Student/approve_leave/<str:id>', Hod_views.STUDENT_APPROVE_LEAVE, name="student_approve_leave"),
    path('hod/Student/disapprove_leave/<str:id>', Hod_views.STUDENT_DISAPPROVE_LEAVE, name="student_disapprove_leave"),



    path('hod/home', Hod_views.HOME, name='hod_home'),
    path('hod/Staff/Add', Hod_views.ADD_STAFF, name='add_staff'),
    path('hod/Staff/View', Hod_views.VIEW_STAFF, name='view_staff'),
    path('hod/Staff/Edit/<int:id>', Hod_views.EDIT_STAFF, name='edit_staff'),
    path('hod/Staff/Update', Hod_views.UPDATE_STAFF, name='update_staff'),
    path('hod/Staff/Delete/<str:admin>', Hod_views.DELETE_STAFF, name='delete_staff'),
    # path('hod/Staff/DeleteAll', Hod_views.DELETE_ALL_STAFF, name='delete_all_staff'),
    path('hod/Staff/Leave_view', Hod_views.STAFF_LEAVE_VIEW, name='staff_leave_view'),
    path('hod/Staff/approve_leave/<str:id>', Hod_views.STAFF_APPROVE_LEAVE, name='staff_approve_leave'),
    path('hod/Staff/disapprove_leave/<str:id>', Hod_views.STAFF_DISAPPROVE_LEAVE, name='staff_disapprove_leave'),

    path('hod/Course/Add',Hod_views.ADD_COURSE,name="add_course"),
    path('hod/Course/View',Hod_views.VIEW_COURSE,name="view_course"),
    path('hod/Course/Edit/<str:id>',Hod_views.EDIT_COURSE,name="edit_course"),
    path('hod/Course/Update',Hod_views.UPDATE_COURSE,name="update_course"),
    path('hod/Course/Delete/<str:id>',Hod_views.DELETE_COURSE,name="delete_course"),

    path('hod/Subject/Add',Hod_views.ADD_SUBJECT,name="add_subject"),
    path('hod/Subject/View',Hod_views.VIEW_SUBJECT,name="view_subject"),
    path('hod/Subject/Edit/<str:id>',Hod_views.EDIT_SUBJECT,name="edit_subject"),
    path('hod/Subject/Update',Hod_views.UPDATE_SUBJECT,name="update_subject"),
    path('hod/Subject/Delete/<str:id>',Hod_views.DELETE_SUBJECT,name="delete_subject"),

    path('hod/Session/Add',Hod_views.ADD_SESSION,name="add_session"),
    path('hod/Session/View',Hod_views.VIEW_SESSION,name="view_session"),
    path('hod/Session/Edit/<str:id>',Hod_views.Edit_SESSION,name="edit_session"),
    path('hod/Session/Update',Hod_views.UPDATE_SESSION,name="update_session"),
    path('hod/Session/Delete/<str:id>',Hod_views.DELETE_SESSION,name="delete_session"),

    path('hod/Staff/Leave_View',Hod_views.STAFF_LEAVE_VIEW,name="staff_leave_view"),
    path('hod/Staff/approve_leave/<str:id>',Hod_views.STAFF_APPROVE_LEAVE,name="staff_approve_leave"),
    path('hod/Staff/disapprove_leave/<str:id>',Hod_views.STAFF_DISAPPROVE_LEAVE,name="staff_disapprove_leave"),
    
    path('hod/View_Attendance',Hod_views.HOD_VIEW_ATTENDANCE,name="hod_view_attendance"),
    path('hod/View_all_student_attendance',Hod_views.VIEW_ALL_STUDENT_ATTENDANCE,name="view_all_student_attendance"),

    path('hod/View_single_student_attendance/<int:student_id>',Hod_views.VIEW_SINGLE_STUDENT_ATTENDANCE,name="view_single_student_attendance"),
    
    

    # This is the staff urls

    path('Staff/Home',staff_views.STAFF_HOME,name="staff_home"),
    path('Staff/Apply_leave',staff_views.STAFF_APPLY_LEAVE,name="staff_apply_leave"),
    path('Staff/Apply_leave_save',staff_views.STAFF_APPLY_LEAVE_SAVE,name="staff_apply_leave_save"),
    path('Staff/Take_Attendance',staff_views.STAFF_TAKE_ATTENDANCE,name="staff_take_attendance"),
    path('Staff/Save_Attendance',staff_views.STAFF_SAVE_ATTENDANCE,name="staff_save_attendance"),
    path('Staff/Attendance_Options',staff_views.STAFF_ATTENDANCE_OPTION,name="staff_attendance_option"),


    path('Staff/Update_Attendance',staff_views.UPDATE_ATTENDANCE,name="update_attendance"),
    
    path('Staff/View_Attendance/', staff_views.VIEW_ATTENDANCE, name="staff_view_attendance"),
    path('Staff/Staff_View_all_student_attendance/', staff_views.VIEW_ALL_STUDENT_ATTENDANCE, name="Staff_view_all_student_attendance"),
    path('Staff/Staff_View_single_student_attendance/<int:student_id>/', staff_views.VIEW_SINGLE_STUDENT_ATTENDANCE, name="Staff_View_single_student_attendance"),



    path('automatic-attendance/', staff_views.automatic_attendance_setup, name='automatic_attendance_setup'),
    # path('process-attendance-image/', staff_views.process_attendance_image, name='process_attendance_image'),
    path('train_model/', staff_views.train_model, name='train_model'),
    # path('submit-automatic-attendance/', staff_views.submit_automatic_attendance, name='submit_automatic_attendance'),
    # path('submit_attendance_data/', staff_views.submit_attendance_data, name='submit_attendance_data'),
  

    #urls for automatic Attendance 
    # path('start_attendance/', staff_views.start_attendance, name='start_attendance'),
    path('process_attendance_video/', staff_views.process_attendance_video, name='process_attendance_video'),


     #student urls

    path('student/student_Home',student_views.STUDENT_HOME,name="student_home"),

    path('student/apply_for_leave',student_views.STUDENT_LEAVE,name="student_leave"),
    path('student/leave_save',student_views.STUDENT_LEAVE_SAVE,name="student_leave_save"),
    path('student/student_home/', student_views.STUDENT_HOME, name='student_home'),
    path('generate_student_card/<int:student_id>/', student_views.generate_student_card, name='generate_student_card'),
    path('student/student_view_attendance/', student_views.STUDENT_VIEW_ATTENDANCE, name='student_view_attendance'),
    path('student/student_view_subject_attendance/', student_views.STUDETN_VIEW_SUBJECT_ATTENDANCE, name='student_view_subject_attendance'),
    path('student/all_subject_attendance/', student_views.ALL_SUBJECT_ATTENDANCE, name='all_subject_attendance'),
    



    # path('test_pdf/', student_views.test_pdf, name='test_pdf'),







 ] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
