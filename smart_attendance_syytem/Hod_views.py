from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from myapp.models import Course,Session_Year,CustomUser,Student,staff,Subject,Session_Year,Staff_leave,Student_leave,Attendance_Report,Attendance
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import os

@login_required(login_url='/')
def HOME(request):

    student_count = Student.objects.all().count()
    staff_count = staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()

    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female
    }


    return render(request, 'hod/home.html',context)




@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        # Retrieve form data
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        course_id = request.POST.get("course_id")
        session_year_id = request.POST.get("session_year_id")
        date_of_birth = request.POST.get("date_of_birth")
        mobile_number = request.POST.get("mobile_number")

        # Check if Session_Year object exists
        session_year_obj = Session_Year.objects.get(id=session_year_id)

        # Check for existing email and username
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return redirect('add_student')

        # Create CustomUser object
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            profile_pic=profile_pic,
            user_type=3
        )
        user.set_password(password)
        user.save()

        # Get Course object
        course_obj = Course.objects.get(id=course_id)

        # Create Student object
        student = Student.objects.create(
            admin=user,
            address=address,
            session_year=session_year_obj,  # Correct field name
            course=course_obj,            # Correct field name
            gender=gender,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number
        )
        messages.success(request, f"{user.first_name} {user.last_name} has been successfully added")
        return redirect("view_student")

    context = {
        'course': course,
        'session_year': session_year,
    }

    return render(request, 'Hod/add_student.html', context)




@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student':student
    }
    return render(request, "Hod/view_student.html",context)


@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = get_object_or_404(Student, id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student': student,
        'course': course,
        'session_year': session_year
    }

    return render(request, 'Hod/edit_student.html', context)



@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        student_id = request.POST.get("student_id")
        session_year_id = request.POST.get("session_year_id")

        # Log the values for debugging
        print(f"Received student_id: {student_id}, session_year_id: {session_year_id}")

        if not student_id or not session_year_id:
            messages.error(request, "Student ID or Session Year ID is missing")
            return redirect("view_student")

        if not student_id.isdigit() or not session_year_id.isdigit():
            messages.error(request, "Invalid Student ID or Session Year ID")
            return redirect("view_student")

        student_id = int(student_id)
        session_year_id = int(session_year_id)

        # Continue with the rest of the code
        try:
            user = CustomUser.objects.get(id=student_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect("view_student")

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.username = request.POST.get("username")
        if request.POST.get("password"):
            user.set_password(request.POST.get("password"))
        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES.get("profile_pic")
        user.save()

        try:
            student = Student.objects.get(admin=user)
        except Student.DoesNotExist:
            messages.error(request, "Student does not exist")
            return redirect("view_student")

        student.address = request.POST.get("address")
        student.gender = request.POST.get("gender")
        student.date_of_birth = request.POST.get("date_of_birth")
        student.mobile_number = request.POST.get("mobile_number")

        try:
            session_year = Session_Year.objects.get(id=session_year_id)
        except Session_Year.DoesNotExist:
            messages.error(request, "Session year does not exist")
            return redirect("view_student")

        student.Session_Year_id = session_year
        student.save()

        messages.success(request, f"{user.first_name} {user.last_name} record updated successfully")
        return redirect("view_student")

    return render(request, 'Hod/edit_student.html')


# @login_required(login_url='/')
# def UPDATE_STUDENT(request):
#     if request.method == 'POST':
#         student_id = request.POST.get("student_id")
#         profile_pic = request.FILES.get("profile_pic")
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         email = request.POST.get("email")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         address = request.POST.get("address")
#         gender = request.POST.get("gender")
#         date_of_birth = request.POST.get("date_of_birth")
#         mobile_number = request.POST.get("mobile_number")
#         session_year_id = request.POST.get("session_year_id")

#         try:
#             user = CustomUser.objects.get(id=student_id)
#         except CustomUser.DoesNotExist:
#             messages.error(request, "User does not exist")
#             return redirect("view_student")

#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.username = username

#         if password:
#             user.set_password(password)
#         if profile_pic:
#             user.profile_pic = profile_pic
#         user.save()

#         try:
#             student = Student.objects.get(admin=user)
#         except Student.DoesNotExist:
#             messages.error(request, "Student does not exist")
#             return redirect("view_student")

#         student.address = address
#         student.gender = gender
#         student.date_of_birth = date_of_birth
#         student.mobile_number = mobile_number

#         try:
#             session_year = Session_Year.objects.get(id=session_year_id)
#         except Session_Year.DoesNotExist:
#             messages.error(request, "Session year does not exist")
#             return redirect("view_student")

#         student.Session_Year_id = session_year

#         student.save()
#         messages.success(request, user.first_name +" " + user.last_name +" "+ " Record updated successfully")
#         return redirect("view_student")

#     return render(request, 'Hod/edit_student.html')





@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    try:
        user = get_object_or_404(CustomUser, id=admin)
        student = get_object_or_404(Student, admin=user)

        # Get the profile picture path
        profile_pic_path = user.profile_pic.path if user.profile_pic else None

        # Delete related attendance reports
        Attendance_Report.objects.filter(student_id=student).delete()

        # Delete related student leave records
        Student_leave.objects.filter(student_id=student).delete()

        # Delete the student record first
        student.delete()

        # Delete the related user record
        user.delete()

        # Check if the profile picture exists and delete it
        if profile_pic_path and os.path.exists(profile_pic_path):
            os.remove(profile_pic_path)

        messages.success(request, "Student deleted successfully")
    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")
    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('view_student')








def STUDENT_LEAVE_VIEW(request):

     student_leave = Student_leave.objects.all()
     context = {
         'student_leave' : student_leave,
     }

     return render(request, 'Hod/student_leave.html',context)


def STUDENT_APPROVE_LEAVE(request,id):
    student_leave = Student_leave.objects.get(id = id)
    student_leave.status = 1
    student_leave.save()

    return redirect('student_leave_view')


def STUDENT_DISAPPROVE_LEAVE(request,id):
    student_leave = Student_leave.objects.get(id = id)
    student_leave.status = 2
    student_leave.save()

    return redirect('student_leave_view')


@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,"Course Are Successfuly Created")
        return redirect('view_course')
    return render(request, "Hod/add_course.html")

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course
    }
    return render(request, "Hod/view_course.html",context)





@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id = id)
    context = {
        'course':course
    }
    return render(request, "Hod/edit_course.html",context)




@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id = course_id)
        course.name = name
        course.save()
        messages.success(request,"Course Are Successfuly Updated")
        return redirect('view_course')
    return render(request,"Hod/edit_course.html")

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,"Course Are Successfuly Deleted")
    return redirect('view_course')
    return None














@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        mobile_number = request.POST.get("mobile_number")
        course_id = request.POST.get("course")

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return redirect("add_staff")
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken.")
            return redirect("add_staff")
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff_member = staff(
                admin=user,
                address=address,
                gender=gender,
                date_of_birth=date_of_birth,
                mobile_number=mobile_number,
                course_id=course_id  # Set the selected course
            )
            staff_member.save()
            messages.success(request, user.first_name +" " + user.last_name +" "+ " Are successfully added")
            return redirect('view_staff')
    else:
        courses = Course.objects.all()  # Fetch all courses for the dropdown
        return render(request, 'Hod/add_staff.html', {'courses': courses})







@login_required(login_url='/')
def VIEW_STAFF(request):
    Staff = staff.objects.all()
    context = {
        'Staff':Staff
    }
    return render(request,'Hod/view_staff.html',context)
@login_required(login_url='/')
def EDIT_STAFF(request, id):
    try:
        staff_instance = staff.objects.get(admin=id)
        context = {
            'staff': staff_instance
        }
        return render(request, 'Hod/edit_staff.html', context)
    except staff.DoesNotExist:
        messages.error(request, "Staff not found")
        return redirect('view_staff')

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == 'POST':
        staff_id = request.POST.get("staff_id")
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        mobile_number = request.POST.get("mobile_number")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            if profile_pic:
                user.profile_pic = profile_pic

            # Check for unique username
            if CustomUser.objects.filter(username=username).exclude(id=staff_id).exists():
                messages.error(request, "Username must be unique")
                return redirect('edit_staff', id=staff_id)

            # Update password only if provided
            if password:
                user.set_password(password)

            user.save()

            staff_instance = staff.objects.get(admin=staff_id)
            staff_instance.gender = gender
            staff_instance.address = address
            staff_instance.date_of_birth = date_of_birth
            staff_instance.mobile_number = mobile_number

            staff_instance.save()
            messages.success(request, "Staff successfully updated")
            return redirect('view_staff')
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found")
        except staff.DoesNotExist:
            messages.error(request, "Staff details not found")

    return render(request, 'Hod/edit_staff.html')






# @login_required(login_url='/')
# def DELETE_ALL_STAFF(request):
#     try:
#         # Delete all related leave records
#         Staff_leave.objects.all().delete()

#         # Delete all related subjects
#         Subject.objects.all().delete()

#         # Delete all staff records
#         staff.objects.all().delete()

#         # Also delete corresponding CustomUser entries for staff
#         CustomUser.objects.filter(user_type=2).delete()

#         messages.success(request, "All staff have been deleted successfully.")
#     except Exception as e:
#         messages.error(request, f"An error occurred while deleting staff: {e}")

#     return redirect('view_staff')









@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    try:
        # Retrieve the user and staff member
        user = get_object_or_404(CustomUser, id=admin)
        staff_member = get_object_or_404(staff, admin=user)

        # Delete related Subject records
        Subject.objects.filter(staff=staff_member).delete()

        # Delete related Staff_leave records
        Staff_leave.objects.filter(staff_id=staff_member).delete()

        # Get the profile picture path
        profile_pic_path = user.profile_pic.path

        # Delete the staff record
        staff_member.delete()

        # Delete the user record
        user.delete()

        # Check if the profile picture exists and delete it
        if os.path.exists(profile_pic_path):
            os.remove(profile_pic_path)

        messages.success(request, "Staff deleted successfully")
    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")
    except staff.DoesNotExist:
        messages.error(request, "Staff does not exist")
    except Exception as e:
        messages.error(request, f"Error deleting staff: {e}")
    return redirect('view_staff')


# @login_required(login_url='/')
# def DELETE_STAFF(request, admin):
#     try:
#         user = get_object_or_404(CustomUser, id=admin)
#         staff_member = get_object_or_404(staff, admin=user)

#         # Get the profile picture path
#         profile_pic_path = user.profile_pic.path

#         # Delete the staff record first
#         staff_member.delete()

#         # Delete the related user record
#         user.delete()

#         # Check if the profile picture exists and delete it
#         if os.path.exists(profile_pic_path):
#             os.remove(profile_pic_path)

#         messages.success(request, "Staff deleted successfully")
#     except CustomUser.DoesNotExist:
#         messages.error(request, "User does not exist")
#     except staff.DoesNotExist:
#         messages.error(request, "Staff does not exist")
#     return redirect('view_staff')

@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    Staff = staff.objects.all()
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        Staff = staff.objects.get(id = staff_id)
        subject = Subject(
            name = subject_name,
            course = course,
            staff = Staff
        )
        subject.save()
        messages.success(request,"Subject Are Successfully Added")
        return redirect('add_subject')
    context = {
        'course':course,
        'Staff':Staff
    }
    return render(request,"Hod/add_subject.html",context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()

    context = {
        'subject':subject
    }
    return render(request,"Hod/view_subject.html",context)




def EDIT_SUBJECT(request,id):

     subject = Subject.objects.get(id = id)
     course = Course.objects.all()
     Staff = staff.objects.all()
     context = {
        'subject':subject,
        'course':course,
        'Staff':Staff
     }
     return render(request,'Hod/edit_subject.html',context)







def UPDATE_SUBJECT(request):
     if request.method == 'POST':
         subject_id = request.POST.get('subject_id')
         subject_name = request.POST.get('subject_name')
         course_id = request.POST.get('course_id')
         staff_id = request.POST.get('staff_id')

         course = Course.objects.get(id = course_id)
         Staff = staff.objects.get(id = staff_id)
         subject = Subject(
             id = subject_id,
             name = subject_name,
             course = course,
             staff = Staff
         )
         subject.save()
         messages.success(request,"Subject Are Successfuly Updated")
         return redirect('view_subject')

     return None

def DELETE_SUBJECT(request,id):

      subject = Subject.objects.filter(id = id)
      subject.delete()
      messages.success(request,"Subject Are Successfuly DELETED")
      return redirect('view_subject')
      return None


def ADD_SESSION(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end  = request.POST.get('session_year_end')

        session = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end
        )
        session.save()
        messages.success(request,"Session Are Successfuly Created")
        return redirect('add_session')

    return render(request,'Hod/add_session.html')

def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context = {
        'session':session
    }
    return render(request,'Hod/view_session.html',context)

def Edit_SESSION(request,id):
   session = Session_Year.objects.filter(id = id)
   context = {
       'session': session
   }

   return render(request,'Hod/edit_session.html',context)


def UPDATE_SESSION(request):
    if request.method == 'POST':
        session_id = request.POST.get("session_id")
        session_year_start = request.POST.get("session_year_start")
        session_year_end = request.POST.get("session_year_end")

        session = Session_Year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end
        )
        session.save()
        messages.success(request,"Session Are Successfuly Updated")
        return redirect('view_session')
    return None

def DELETE_SESSION(request,id):

    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request,"Session Are Successfuly Deleted")
    return redirect('view_session')
    return None

def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_leave.objects.all()
    context = {
        'staff_leave' :staff_leave
    }
    return render(request,'Hod/staff_leave.html',context)

def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')
    return None


def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')
    return None





# def HOD_VIEW_ATTENDANCE(request):
#     courses = Course.objects.all()
#     session_years = Session_Year.objects.all()
#     action = request.GET.get('action', None)

#     if request.method == 'POST' and action == 'get_student':
#         course_id = request.POST.get('course_id')
#         session_id = request.POST.get('session_id')
#         selected_course = Course.objects.get(id=course_id)
#         selected_session_year = Session_Year.objects.get(id=session_id)
#         subjects = Subject.objects.filter(course_id=course_id)
#         attendance_dates = Attendance.objects.filter(subject_id__in=subjects).values('attendance_date').distinct()

#         context = {
#             'action': action,
#             'courses': courses,
#             'session_years': session_years,
#             'selected_course': selected_course,
#             'selected_session_year': selected_session_year,
#             'subjects': subjects,
#             'attendance_dates': attendance_dates,
#         }
#         return render(request, 'Hod/hod_view_attendance.html', context)

#     context = {
#         'courses': courses,
#         'session_years': session_years,
#     }
#     return render(request, 'Hod/hod_view_attendance.html', context)


# def HOD_VIEW_ATTENDANCE(request):
#     if request.method == "POST" and request.GET.get('action') == "get_student":
#         course_id = request.POST.get('course_id')
#         session_id = request.POST.get('session_id')
#         selected_course = Course.objects.get(id=course_id)
#         selected_session_year = Session_Year.objects.get(id=session_id)
#         subjects = Subject.objects.filter(course_id=course_id)
#         action = "get_subjects"
#         attendance_dates = Attendance.objects.filter(subject_id__in=subjects).values('attendance_date').distinct()

#         context = {
#             "courses": Course.objects.all(),
#             "session_years": Session_Year.objects.all(),
#             "selected_course": selected_course,
#             "selected_session_year": selected_session_year,
#             "subjects": subjects,
#             "action": action,
#             'attendance_dates': attendance_dates,
#         }
#         return render(request, "Hod/hod_view_attendance.html", context)

#     elif request.method == "POST" and request.GET.get('action') == "submit_attendance":
#         subject_id = request.POST.get('subject_id')
#         selected_subject = Subject.objects.get(id=subject_id)
#         attendance_dates = Attendance.objects.filter(subject_id=subject_id).values('date').distinct()

#         context = {
#             "selected_subject": selected_subject,
#             "attendance_dates": attendance_dates,
#         }
#         return render(request, "Hod/hod_view_attendance.html", context)

#     context = {
#         "courses": Course.objects.all(),
#         "session_years": Session_Year.objects.all(),
#     }
#     return render(request, "Hod/hod_view_attendance.html", context)

def HOD_VIEW_ATTENDANCE(request):
    if request.method == "POST" and request.GET.get('action') == "get_student":
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        selected_course = Course.objects.get(id=course_id)
        selected_session_year = Session_Year.objects.get(id=session_id)
        subjects = Subject.objects.filter(course_id=course_id)
        action = "get_subjects"
        attendance_dates = Attendance.objects.filter(subject_id__in=subjects).values('attendance_date').distinct()

        context = {
            "courses": Course.objects.all(),
            "session_years": Session_Year.objects.all(),
            "selected_course": selected_course,
            "selected_session_year": selected_session_year,
            "subjects": subjects,
            "action": action,
            'attendance_dates': attendance_dates,
        }
        return render(request, "Hod/hod_view_attendance.html", context)

    elif request.method == "POST" and request.GET.get('action') == "submit_attendance":
        subject_id = request.POST.get('subject_id')
        selected_subject = Subject.objects.get(id=subject_id)
        attendance_dates = Attendance.objects.filter(subject_id=subject_id).values('attendance_date').distinct()  # Changed 'date' to 'attendance_date'

        context = {
            "selected_subject": selected_subject,
            "attendance_dates": attendance_dates,
        }
        return render(request, "Hod/hod_view_attendance.html", context)

    context = {
        "courses": Course.objects.all(),
        "session_years": Session_Year.objects.all(),
    }
    return render(request, "Hod/hod_view_attendance.html", context)




from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError



def VIEW_ALL_STUDENT_ATTENDANCE(request):
    if request.method == 'POST' and request.GET.get('action') == 'submit_attendance':
        subject_id = request.POST.get('subject_id')
        attendance_date = request.POST.get('attendance_date')

        try:
            parsed_date = datetime.strptime(attendance_date, '%b. %d, %Y')
            formatted_date = parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            return render(request, 'Hod/hod_all_student_view_attendance.html', {'error': 'Invalid date format.'})

        attendance_records = Attendance.objects.filter(subject_id=subject_id, attendance_date=formatted_date)

        if attendance_records.exists():
            students_attendance = []

            for attendance in attendance_records:
                attendance_reports = Attendance_Report.objects.filter(attendance_id=attendance)

                for report in attendance_reports:
                    student_info = {
                        'student_id': report.student_id.admin.id,
                        'name': f"{report.student_id.admin.first_name} {report.student_id.admin.last_name}",
                        'profile_pic': report.student_id.admin.profile_pic.url if report.student_id.admin.profile_pic else None,
                        'status': report.status,
                        'selected_subject': Subject.objects.get(id=subject_id).name,
                        'attendance_date': attendance.attendance_date.strftime('%Y-%m-%d')
                    }
                    students_attendance.append(student_info)

            context = {
                'students': students_attendance,
                'selected_subject': Subject.objects.get(id=subject_id),
                'attendance_date': formatted_date,
            }

            # Debug: Print the context to the console to check the data
            print(context)

            return render(request, 'Hod/hod_all_student_view_attendance.html', context)
        else:
            return render(request, 'Hod/hod_all_student_view_attendance.html', {'error': 'No attendance records found.'})

    return HttpResponseRedirect(reverse('view_single_student_attendance'))



from datetime import datetime

import calendar
from datetime import date


from collections import Counter
from datetime import date
import calendar

from django.utils.dateparse import parse_date
from collections import Counter
from datetime import date
import calendar

def VIEW_SINGLE_STUDENT_ATTENDANCE(request, student_id):
    try:
        student = Student.objects.get(admin_id=student_id)
        attendance_records = Attendance_Report.objects.filter(student_id=student)

        # Generate all days of the selected month
        if request.method == "POST":
            month_year = request.POST['month']
            year, month = map(int, month_year.split('-'))
        else:
            today = date.today()
            year, month = today.year, today.month

        all_days_of_month = [
            date(year, month, day)
            for day in range(1, calendar.monthrange(year, month)[1] + 1)
        ]

        # Create a dictionary for easy lookup of attendance records by day
        attendance_dict = {
            attendance.attendance_id.attendance_date: attendance
            for attendance in attendance_records
        }

        # Count the number of present, absent, and leave days
        attendance_statuses = [record.status for record in attendance_records if record.attendance_id.attendance_date.month == month]
        attendance_count = Counter(attendance_statuses)
        present_count = attendance_count.get('present', 0)
        absent_count = attendance_count.get('absent', 0)
        leave_count = attendance_count.get('leave', 0)

        context = {
            'student': student,
            'attendance_records': attendance_dict,
            'all_days_of_month': all_days_of_month,
            'present_count': present_count,
            'absent_count': absent_count,
            'leave_count': leave_count,
        }
        return render(request, "Hod/hod_view_single_student_attendance.html", context)
    except Student.DoesNotExist:
         return render(request, "Hod/hod_view_single_student_attendance.html", {'error': 'Student not found.'})




# def VIEW_SINGLE_STUDENT_ATTENDANCE(request, student_id):
#     try:
#         student = Student.objects.get(admin_id=student_id)
#         attendance_records = Attendance_Report.objects.filter(student_id=student)

#         # Generate all days of the selected month
#         if request.method == "POST":
#             month_year = request.POST['month']
#             year, month = map(int, month_year.split('-'))
#         else:
#             today = date.today()
#             year, month = today.year, today.month

#         all_days_of_month = [
#             date(year, month, day)
#             for day in range(1, calendar.monthrange(year, month)[1] + 1)
#         ]

#         # Create a dictionary for easy lookup of attendance records by day
#         attendance_dict = {
#             attendance.attendance_id.attendance_date: attendance
#             for attendance in attendance_records
#         }

#         # Count the number of present, absent, and leave days
#         attendance_statuses = [record.status for record in attendance_records if record.attendance_id.attendance_date.month == month]
#         attendance_count = Counter(attendance_statuses)
#         present_count = attendance_count.get('present', 0)
#         absent_count = attendance_count.get('absent', 0)
#         leave_count = attendance_count.get('leave', 0)

#         context = {
#             'student': student,
#             'attendance_records': attendance_dict,
#             'all_days_of_month': all_days_of_month,
#             'present_count': present_count,
#             'absent_count': absent_count,
#             'leave_count': leave_count,
#         }

#         return render(request, "Hod/hod_view_single_student_attendance.html", context)
#     except Student.DoesNotExist:
#         return render(request, "Hod/hod_view_single_student_attendance.html", {'error': 'Student not found.'})






