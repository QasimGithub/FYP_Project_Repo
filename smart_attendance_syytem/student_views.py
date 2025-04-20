from django.shortcuts import render, redirect ,get_object_or_404
from myapp.models import Student,Student_leave
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
import base64
from django.template import TemplateDoesNotExist
import tempfile
from weasyprint import HTML, CSS
from myapp.models import Student, Subject, Attendance, Attendance_Report
from cryptography.fernet import Fernet
from django.conf import settings






@login_required(login_url='/login/')
def STUDENT_HOME(request):
    user = request.user  # Get the logged-in user
    try:
        student_instance = Student.objects.get(admin=user)  # Get the Student instance related to the logged-in user
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://example.com/attendance/{student_instance.id}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        # Convert QR code image to a byte stream and encode it in base64
        qr_bytes = BytesIO()
        qr_img.save(qr_bytes, format='PNG')
        qr_bytes.seek(0)
        qr_code_base64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')

        context = {
            'student': student_instance,
            'qr_code': qr_code_base64,
        }
        return render(request, 'student/student_home.html', context)

    except Student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('some_default_view')









# from cryptography.fernet import Fernet

# # Generate a new key
# key = Fernet.generate_key()
# print(key.decode())


# import secrets

# def generate_key():
#     # Generate a secure random key
#     key = secrets.token_urlsafe(32)
#     return key

# if __name__ == "__main__":
#     print(generate_key())


# # Add this line with your generated key
# SECRET_ENCRYPTION_KEY = 'your-generated-key-here'


# # Initialize the cipher with the key from settings
# cipher_suite = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())



# def generate_qr_code(student):
#     # Initialize Fernet with the secret key
#     cipher_suite = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())
    
#     # Encrypt student data
#     student_data = f"Name: {student.admin.first_name} {student.admin.last_name}, Email: {student.admin.email}"
#     encrypted_data = cipher_suite.encrypt(student_data.encode()).decode()

#     # Generate QR code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(encrypted_data)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
    
#     # Convert image to base64
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     img_str = base64.b64encode(buffer.getvalue()).decode()
    
#     return img_str



# def generate_student_card(request, student_id):
#     try:
#         # Get the student object
#         student = Student.objects.get(id=student_id)
        
#         # Initialize Fernet with the secret key
#         cipher_suite = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())
        
#         # Encrypt student data
#         encrypted_data = cipher_suite.encrypt(
#             f'Student ID: {student.id}, Name: {student.admin.first_name} {student.admin.last_name}'.encode()
#         ).decode()

#         # Generate QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(encrypted_data)
#         qr.make(fit=True)
#         img = qr.make_image(fill='black', back_color='white')
        
#         # Convert image to base64
#         buffered = BytesIO()
#         img.save(buffered, format="PNG")
#         qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

#         # Render the HTML template with student data
#         html_string = render_to_string('student/student_card.html', {
#             'student': student,
#             'qr_code': qr_code_base64,
#         })
        
#         # Create a response object with the PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="student_card_{student_id}.pdf"'
        
#         # Generate the PDF
#         pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])
#         response.write(pdf)
        
#         return response
#     except Student.DoesNotExist:
#         return HttpResponse("Student not found", status=404)
#     except TemplateDoesNotExist:
#         return HttpResponse("Template not found", status=404)
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}", status=500)










# old code is lower 


def generate_qr_code(student):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"Name: {student.admin.first_name} {student.admin.last_name}, Email: {student.admin.email}"
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str









def generate_student_card(request, student_id):
    try:
        # Get the student object
        student = Student.objects.get(id=student_id)
        
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Student ID: {student.id}, Name: {student.admin.first_name} {student.admin.last_name}')
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Render the HTML template with student data
        html_string = render_to_string('student/student_card.html', {
            'student': student,
            'qr_code': qr_code_base64,
        })
        
        # Create a response object with the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_card_{student_id}.pdf"'
        
        # Generate the PDF
        pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])
        response.write(pdf)
        

        
        return response
    except Student.DoesNotExist:
        return HttpResponse("Student not found", status=404)
    except TemplateDoesNotExist:
        return HttpResponse("Template not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





# old code his upper








def STUDENT_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    student_leave_history = Student_leave.objects.filter(student_id = student)
    context = {
        'student_leave_history': student_leave_history
    }
    return render(request,'student/apply_leave.html',context)

def STUDENT_LEAVE_SAVE(request):

    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_id = Student.objects.get(admin = request.user.id)

        student_leave = Student_leave (
            student_id = student_id,
            date = leave_date,
            message = leave_message
        )
        student_leave.save()
        messages.success(request,'Leave are Successfully send')

        return redirect('student_leave')
    




def STUDENT_VIEW_ATTENDANCE(request):
    # Get the logged-in student
    student = get_object_or_404(Student, admin=request.user)
    
    # Fetch the subjects related to the student's course
    subjects = student.course.subject_set.all()
    
    context = {
        'subjects': subjects
    }
    return render(request, 'student/student_view_attendance.html', context)






from django.shortcuts import render
from django.utils.dateparse import parse_date
from collections import Counter
from datetime import date
import calendar
import datetime



def STUDETN_VIEW_SUBJECT_ATTENDANCE(request):
    student = get_object_or_404(Student, admin=request.user)
    
    subjects = student.course.subject_set.all()
    
    month = request.GET.get('month', datetime.date.today().strftime('%Y-%m'))
    year, month = map(int, month.split('-'))
    start_date = datetime.date(year, month, 1)
    end_date = (start_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
    attendance_records = Attendance_Report.objects.filter(
        student_id=student,
        attendance_id__attendance_date__range=[start_date, end_date]
    ).values('attendance_id__attendance_date', 'status')
    
    # Prepare attendance data for the calendar
    all_days_of_month = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    attendance_dict = {record['attendance_id__attendance_date']: record['status'] for record in attendance_records}

    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    leave_count = attendance_records.filter(status='leave').count()

    context = {
        'student': student,
        'subjects': subjects,
        'all_days_of_month': all_days_of_month,
        'attendance_records': attendance_dict,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
    }
    
    return render(request, "student/student_view_subject_attendance.html", context)




def ALL_SUBJECT_ATTENDANCE(request):
    student = get_object_or_404(Student, admin=request.user)
    
    # Get the student's course and session year
    course = student.course
    session_year = student.session_year
    
    # Fetch all subjects for the student's course
    subjects = Subject.objects.filter(course=course)
    
    # Prepare data for the chart
    chart_data = []
    for subject in subjects:
        # Calculate attendance records for the current month
        current_month = datetime.date.today().strftime('%Y-%m')
        year, month = map(int, current_month.split('-'))
        start_date = datetime.date(year, month, 1)
        end_date = (start_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        
        # Fetch attendance records for the subject
        attendance_records = Attendance_Report.objects.filter(
            student_id=student,
            attendance_id__subject_id=subject,
            attendance_id__attendance_date__range=[start_date, end_date]
        )
        
        total_days = (end_date - start_date).days + 1
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        leave_count = attendance_records.filter(status='leave').count()
        
        # Calculate percentages
        present_percentage = (present_count / total_days) * 100
        absent_percentage = (absent_count / total_days) * 100
        leave_percentage = (leave_count / total_days) * 100
        
        chart_data.append({
            'subject': subject.name,
            'present_percentage': present_percentage,
            'absent_percentage': absent_percentage,
            'leave_percentage': leave_percentage
        })

    context = {
        'chart_data': chart_data,
    }
    
    return render(request, "student/all_subject_attendance.html", context)
