from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import staff,Staff_leave,Subject,Session_Year,Student,Attendance,Attendance_Report,Course,CustomUser
from django.contrib import messages
from django.http import HttpResponse
import cv2
import face_recognition
import base64
import numpy as np
import os
import json
from django.http import JsonResponse





@login_required(login_url='/login/')
def STAFF_HOME(request):
    user = request.user  # Get the logged-in user
    staff_instance = staff.objects.get(admin=user)  # Assuming there is a Staff model related to the CustomUser model
    context = {
        'staff': staff_instance
    }
    return render(request, 'Staff/staff_home.html', context)


    
def STAFF_APPLY_LEAVE(request):
    Staff = staff.objects.filter(admin = request.user.id)
    for i in Staff:
        st_id = i.id

        staff_leave_history = Staff_leave.objects.filter(staff_id = st_id)
        context = {
            'staff_leave_history' : staff_leave_history
        }
    return render(request, 'Staff/apply_leave.html',context)



def STAFF_APPLY_LEAVE_SAVE(request):

    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        Staff = staff.objects.get(admin = request.user.id)

        leave = Staff_leave(
            staff_id = Staff,
            date = leave_date,
            message = leave_message
        )
        leave.save()
        messages.success(request,'Leave successfully send ')
        return redirect('staff_apply_leave')

    return None








@login_required(login_url='/')
def STAFF_TAKE_ATTENDANCE(request):
    staff_id = staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff=staff_id)
    session_years = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = []

    if action == 'get_student' and request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')

        # Check if subject_id and session_id are provided
        if not subject_id and not session_id:
            messages.error(request, "You did not select a subject or session year.")
            return render(request, "Staff/take_attendance.html", {
                'subjects': subjects,
                'session_years': session_years,
                'action': action
            })
        elif not subject_id:
            messages.error(request, "You did not select a subject.")
            return render(request, "Staff/take_attendance.html", {
                'subjects': subjects,
                'session_years': session_years,
                'action': action
            })
        elif not session_id:
            messages.error(request, "You did not select a session year.")
            return render(request, "Staff/take_attendance.html", {
                'subjects': subjects,
                'session_years': session_years,
                'action': action
            })

        try:
            # Convert subject_id and session_id to integers if necessary
            subject_id = int(subject_id)
            session_id = int(session_id)

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_id)

            # Filter students based on the selected subject
            students = Student.objects.filter(course_id=get_subject.course.id)

        except Subject.DoesNotExist:
            messages.error(request, "The selected subject does not exist.")
        except Session_Year.DoesNotExist:
            messages.error(request, "The selected session year does not exist.")
        except ValueError:
            messages.error(request, "Invalid subject or session year ID provided.")

    context = {
        'subjects': subjects,
        'session_years': session_years,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students
    }
    return render(request, "Staff/take_attendance.html", context)






def STAFF_SAVE_ATTENDANCE(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_id)

        # Check if attendance already exists
        if Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date, session_year_id=get_session_year).exists():
            messages.error(request, "Attendance for this subject on this date has already been submitted.")
            return redirect('staff_take_attendance')

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        # Iterate over all students
        students = Student.objects.filter(course_id=get_subject.course.id, session_year_id=get_session_year.id)
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                attendance_report = Attendance_Report(
                    student_id=student,
                    attendance_id=attendance,
                    status=status,
                )
                attendance_report.save()

        messages.success(request, "Attendance has been successfully recorded.")
        return redirect('staff_take_attendance')

    return HttpResponse("Invalid method")







def UPDATE_ATTENDANCE(request):
    if request.method == 'POST':
        action = request.GET.get('action')
        
        if action == 'get_student':
            # Existing code to fetch students based on date, subject, and session year
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')

            subject = get_object_or_404(Subject, id=subject_id)
            session_year = get_object_or_404(Session_Year, id=session_id)

            # Check if attendance exists for the selected date, subject, and session year
            attendance_qs = Attendance.objects.filter(subject_id=subject, session_year_id=session_year, attendance_date=attendance_date)
            
            if attendance_qs.exists():
                # Attendance exists, proceed to fetch and display it
                attendance = attendance_qs.first()
                attendance_reports = Attendance_Report.objects.filter(attendance_id=attendance)

                # Creating a list of tuples containing student and their attendance status
                attendance_records = [(report.student_id, report.status) for report in attendance_reports]

                context = {
                    'action': True,
                    'get_subject': subject,
                    'get_session_year': session_year,
                    'get_attendance_date': attendance_date,
                    'attendance_records': attendance_records,
                }
                return render(request, 'Staff/update_attendance.html', context)
            else:
                # Attendance not found, show an error message
                subjects = Subject.objects.filter(staff=request.user.staff)
                session_years = Session_Year.objects.all()
                context = {
                    'subjects': subjects,
                    'session_years': session_years,
                    'error': f'No attendance record found for the selected date: {attendance_date}.',
                }
                return render(request, 'Staff/update_attendance.html', context)

        else:
            # Handle attendance update submission
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')

            subject = get_object_or_404(Subject, id=subject_id)
            session_year = get_object_or_404(Session_Year, id=session_id)
            attendance = get_object_or_404(Attendance, subject_id=subject, session_year_id=session_year, attendance_date=attendance_date)

            # Iterate through the attendance records and update the status
            attendance_reports = Attendance_Report.objects.filter(attendance_id=attendance)
            for report in attendance_reports:
                student_id = report.student_id.id
                new_status = request.POST.get(f'status_{student_id}')
                report.status = new_status
                report.save()

            # Redirect or show a success message after updating
            messages.success(request, 'Attendance updated successfully.')
            return redirect('update_attendance')

    else:
        # Fetch all subjects associated with the logged-in teacher
        subjects = Subject.objects.filter(staff=request.user.staff)
        session_years = Session_Year.objects.all()

        context = {
            'subjects': subjects,
            'session_years': session_years,
        }

        return render(request, 'Staff/update_attendance.html', context)




def STAFF_ATTENDANCE_OPTION(request):
    return render(request,'Staff/attendance_option.html')






#1
def automatic_attendance_setup(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')

        # Check if attendance already exists
        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_id)
        if Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date, session_year_id=get_session_year).exists():
            messages.error(request, "Attendance for this subject on this date has already been submitted.")
            return redirect('staff_attendance_option')

        # Render webcam interface for attendance
        return render(request, 'Staff/automatic_attendance.html', {
            'subject_id': subject_id,
            'session_id': session_id,
            'attendance_date': attendance_date
        })

    # Get subjects taught by the current staff member
    subjects = Subject.objects.filter(staff=request.user.staff)
    session_years = Session_Year.objects.all()

    # Debugging output to check fetched subjects
    if not subjects.exists():
        print("No subjects found for this staff member.")
    else:
        print(f"Fetched subjects: {subjects}")

    return render(request, 'Staff/automatic_attendance_setup.html', {
        'subjects': subjects,
        'session_years': session_years
    })







import cv2
import face_recognition
import numpy as np
import base64
import json
from django.http import JsonResponse
from myapp.models import Student, Attendance, Attendance_Report, Session_Year, Subject



#functionlly working properly
def train_model(selected_session_year):
    known_encodings = []
    known_names = []

    students_in_session = Student.objects.filter(session_year_id=selected_session_year)

    for student in students_in_session:
        profile_pic_path = student.admin.profile_pic.path
        if os.path.exists(profile_pic_path):
            image = face_recognition.load_image_file(profile_pic_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_encodings.append(encoding[0])
                known_names.append(f"{student.admin.first_name} {student.admin.last_name}")
            else:
                print(f"Encoding not found for {student.admin.first_name} {student.admin.last_name}")
        else:
            print(f"Image not found for {student.admin.first_name} {student.admin.last_name}")

    return known_encodings, known_names


from django.http import JsonResponse
import requests


#functionaly working properly previous code 2nd
# def process_attendance_video(request):
#     if request.method == 'POST':
#         selected_session_year = request.POST.get('session_id')
#         known_encodings, known_names = train_model(selected_session_year)

#         video_capture = cv2.VideoCapture(0)  # Open the default camera
#         present_students = []

#         while True:
#             ret, frame = video_capture.read()
#             if not ret:
#                 break

#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(known_encodings, face_encoding)
#                 name = "Unknown"

#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     name = known_names[first_match_index]
#                     border_color = (0, 255, 0)  # Green
#                 else:
#                     border_color = (0, 0, 255)  # Red

#                 # Draw the rectangle around the face
#                 cv2.rectangle(frame, (left, top), (right, bottom), border_color, 2)

#                 # Draw the name below the rectangle
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left, top - 10), font, 0.5, border_color, 1)

#                 if name != "Unknown":
#                     present_students.append(name)

#             # Display the resulting frame
#             cv2.imshow('Video', frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         video_capture.release()
#         cv2.destroyAllWindows()

#         # Store present students in session
#         request.session['present_students'] = present_students

#         # Process attendance data and return the result
#         unique_faces = list(set(present_students))
#         return JsonResponse({'faces': unique_faces})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)


def process_attendance_video(request):
    if request.method == 'POST':
        selected_session_year = request.POST.get('session_id')
        subject_id = request.POST.get('subject_id')
        attendance_date = request.POST.get('attendance_date')
        
        # Train model with student faces
        known_encodings, known_names = train_model(selected_session_year)

        video_capture = cv2.VideoCapture(0)  # Open the default camera
        present_students = []

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                    border_color = (0, 255, 0)  # Green
                else:
                    border_color = (0, 0, 255)  # Red

                # Draw the rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), border_color, 2)

                # Draw the name below the rectangle
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, top - 10), font, 0.5, border_color, 1)

                if name != "Unknown":
                    present_students.append(name)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            # If 's' key is pressed, save attendance to the database
            if cv2.waitKey(1) & 0xFF == ord('s'):
                # Retrieve the subject and session year
                get_subject = Subject.objects.get(id=subject_id)
                get_session_year = Session_Year.objects.get(id=selected_session_year)
                
                # Create the attendance record
                attendance = Attendance(
                    subject_id=get_subject,
                    attendance_date=attendance_date,
                    session_year_id=get_session_year,
                )
                attendance.save()

                # Mark students as present or absent
                students = Student.objects.filter(course_id=get_subject.course.id, session_year_id=get_session_year.id)
                for student in students:
                    status = 'present' if f"{student.admin.first_name} {student.admin.last_name}" in present_students else 'absent'
                    attendance_report = Attendance_Report(
                        student_id=student,
                        attendance_id=attendance,
                        status=status,
                    )
                    attendance_report.save()

                # Notify success
                messages.success(request, "Attendance has been successfully recorded.")
                break  # Break out of the loop once attendance is saved

            # If 'q' key is pressed, quit the loop without saving
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        return redirect('staff_attendance_option')

    return JsonResponse({'error': 'Invalid request method'}, status=405)




# #functionaly working properly previous code 
# def process_attendance_video(request):
#     if request.method == 'POST':
#         selected_session_year = request.POST.get('session_id')
#         known_encodings, known_names = train_model(selected_session_year)

#         video_capture = cv2.VideoCapture(0)  # Open the default camera

#         attendance_data = []

#         while True:
#             ret, frame = video_capture.read()
#             if not ret:
#                 break

#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             face_locations = face_recognition.face_locations(rgb_frame)
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             faces = []
#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(known_encodings, face_encoding)
#                 name = "Unknown"

#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     name = known_names[first_match_index]

#                 faces.append({
#                     'name': name,
#                     'x': left,
#                     'y': top,
#                     'width': right - left,
#                     'height': bottom - top
#                 })

#                 attendance_data.append(name)

#             # Break the loop based on some condition or time limit
#             # For now, break the loop after processing a single frame
#             break

#         video_capture.release()

#         # Process attendance data and return the result
#         unique_faces = list(set(attendance_data))
#         return JsonResponse({'faces': unique_faces})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def submit_attendance_data(request, present_students):
#     subject_id = request.POST.get('subject_id')
#     session_id = request.POST.get('session_id')
#     attendance_date = request.POST.get('attendance_date')

#     # Prepare the POST data
#     post_data = {
#         'subject_id': subject_id,
#         'session_id': session_id,
#         'attendance_date': attendance_date,
#         'present_students': ','.join(present_students),  # Convert list to comma-separated string
#     }

#     # Send the POST request to submit_automatic_attendance
#     response = requests.post(request.build_absolute_uri('/submit_automatic_attendance/'), data=post_data)

#     return JsonResponse(response.json())

#functionly working properly  2nd
# def submit_automatic_attendance(request):
#     if request.method == 'POST':
#         subject_id = request.POST.get('subject_id')
#         session_id = request.POST.get('session_id')
#         attendance_date = request.POST.get('attendance_date')

#         # Retrieve the present students from the session
#         present_students = request.session.get('present_students', [])

#         get_subject = Subject.objects.get(id=subject_id)
#         get_session_year = Session_Year.objects.get(id=session_id)
#         attendance = Attendance(
#             subject_id=get_subject,
#             attendance_date=attendance_date,
#             session_year_id=get_session_year,
#         )
#         attendance.save()

#         students = Student.objects.filter(course_id=get_subject.course.id, session_year_id=get_session_year.id)
#         for student in students:
#             status = 'present' if f"{student.admin.first_name} {student.admin.last_name}" in present_students else 'absent'
#             attendance_report = Attendance_Report(
#                 student_id=student,
#                 attendance_id=attendance,
#                 status=status,
#             )
#             attendance_report.save()

#         messages.success(request, "Attendance has been successfully recorded.")
#         return redirect('staff_attendance_option')

#     return JsonResponse({"error": "Invalid method"}, status=405)







# # def start_attendance(request):
# #     return render(request, 'start_attendance.html')


# # def train_model(profile_pic_path, selected_session_year):
#     known_encodings = []
#     known_names = []

#     # Fetch students from the selected session year
#     students_in_session = Student.objects.filter(session_year_id=selected_session_year)

#     for student in students_in_session:
#         filename = f"{student.id}.jpg"  # Assuming the filename is the student's ID
#         image_path = os.path.join(profile_pic_path, filename)

#         if os.path.exists(image_path):
#             image = face_recognition.load_image_file(image_path)
#             encoding = face_recognition.face_encodings(image)
#             if encoding:  # Check if encoding is found
#                 known_encodings.append(encoding[0])
#                 known_names.append(student.name)  # Use the student's name

#     return known_encodings, known_names




# def process_attendance_image(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         image_data = data.get('image')

#         # Decode the image
#         image_data = image_data.split(',')[1]
#         image_bytes = base64.b64decode(image_data)
#         np_arr = np.frombuffer(image_bytes, np.uint8)
#         img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         # Convert image to RGB for face_recognition
#         rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         # Find faces in the image
#         face_locations = face_recognition.face_locations(rgb_img)
#         face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

#         # Get trained encodings and names
#         known_encodings, known_names = train_model('media/profile_pic')

#         faces = []
#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_encodings, face_encoding)
#             name = "Unknown"

#             # If a match is found
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_names[first_match_index]

#             # Append face details
#             faces.append({
#                 'name': name,
#                 'x': left,
#                 'y': top,
#                 'width': right - left,
#                 'height': bottom - top
#             })

#         return JsonResponse({'faces': faces})

#     return JsonResponse({'faces': []})


# def train_model(profile_pic_path):
#     known_encodings = []
#     known_names = []

#     # Iterate over each image in the profile_pics folder
#     for filename in os.listdir(profile_pic_path):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             image_path = os.path.join(profile_pic_path, filename)
#             image = face_recognition.load_image_file(image_path)
#             encoding = face_recognition.face_encodings(image)
#             if encoding:
#                 known_encodings.append(encoding[0])
#                 # Extract the student's name from the filename
#                 student_name = filename.split('.')[0]
#                 known_names.append(student_name)
    
#     return known_encodings, known_names

# #1
# #functionaly working
# def submit_automatic_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')
        present_students = request.POST.getlist('present_students[]')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_id)
        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year,
        )
        attendance.save()

        students = Student.objects.filter(course_id=get_subject.course.id, session_year_id=get_session_year.id)
        for student in students:
            status = 'present' if str(student.id) in present_students else 'absent'
            attendance_report = Attendance_Report(
                student_id=student,
                attendance_id=attendance,
                status=status,
            )
            attendance_report.save()

        messages.success(request, "Attendance has been successfully recorded.")
        return redirect('staff_attendance_option')

    return HttpResponse("Invalid method")













from django.shortcuts import render, redirect, get_object_or_404





# def VIEW_ATTENDANCE(request):
#     if request.method == 'POST':
#         action = request.GET.get('action')
#         if action == 'get_student':
#             subject_id = request.POST.get('subject_id')
#             session_id = request.POST.get('session_id')

#             if subject_id and session_id:
#                 selected_subject = get_object_or_404(Subject, id=subject_id)
#                 selected_session_year = get_object_or_404(Session_Year, id=session_id)

#                 # Filter Attendance based on session year and subject
#                 attendance_dates = Attendance.objects.filter(
#                     session_year_id=selected_session_year,
#                     subject_id=selected_subject
#                 ).values('attendance_date').distinct()

#                 context = {
#                     'selected_subject': selected_subject,
#                     'selected_session_year': selected_session_year,
#                     'attendance_dates': attendance_dates,
#                     'action': 'show_dates'
#                 }
#                 return render(request, 'Staff/Staff_view_attendance.html', context)
        
#         elif action == 'submit_attendance':
#             # Handle the attendance view form submission here
#             pass

#     else:
#         # Get the current logged-in staff member
#         current_user = request.user
#         current_staff = get_object_or_404(staff, admin=current_user)

#         # Filter subjects by the current staff member
#         subjects = Subject.objects.filter(staff=current_staff)
#         session_years = Session_Year.objects.all()

#         context = {
#             'subjects': subjects,
#             'session_years': session_years,
#             'action': None
#         }
#         return render(request, 'Staff/Staff_view_attendance.html', context)



def VIEW_ATTENDANCE(request):
    if request.method == 'POST':
        action = request.GET.get('action')
        if action == 'get_student':
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')

            if subject_id and session_id:
                selected_subject = get_object_or_404(Subject, id=subject_id)
                selected_session_year = get_object_or_404(Session_Year, id=session_id)

                # Filter Attendance based on session year and subject
                attendance_dates = Attendance.objects.filter(
                    session_year_id=selected_session_year,
                    subject_id=selected_subject
                ).values('attendance_date').distinct()

                context = {
                    'selected_subject': selected_subject,
                    'selected_session_year': selected_session_year,
                    'attendance_dates': attendance_dates,
                    'action': 'show_dates'
                }
                return render(request, 'Staff/Staff_view_attendance.html', context)

    else:
        # Get the current logged-in staff member
        current_user = request.user
        current_staff = get_object_or_404(staff, admin=current_user)

        # Filter subjects by the current staff member
        subjects = Subject.objects.filter(staff=current_staff)
        session_years = Session_Year.objects.all()

        context = {
            'subjects': subjects,
            'session_years': session_years,
            'action': None
        }
        return render(request, 'Staff/Staff_view_attendance.html', context)





from datetime import datetime

def VIEW_ALL_STUDENT_ATTENDANCE(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        attendance_date = request.POST.get('attendance_date')

        # Parse the date to the format YYYY-MM-DD
        try:
            parsed_date = datetime.strptime(attendance_date, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format
            return render(request, 'Staff/Staff_view_attendance.html', {'error': 'Invalid date format'})

        selected_subject = get_object_or_404(Subject, id=subject_id)
        attendance_records = Attendance_Report.objects.filter(
            attendance_id__subject_id=selected_subject,
            attendance_id__attendance_date=parsed_date
        )

        context = {
            'selected_subject': selected_subject,
            'selected_date': parsed_date,
            'attendance_records': attendance_records
        }

        return render(request, 'Staff/Staff_all_student_view_attendance.html', context)
    else:
        # Handle the GET request case or redirect if needed
        return render(request, 'Staff/Staff_view_attendance.html')




from datetime import datetime, timedelta

from calendar import monthrange

from django.shortcuts import render, get_object_or_404



from datetime import datetime



from datetime import datetime, timedelta
from calendar import monthrange
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse




import calendar



def VIEW_SINGLE_STUDENT_ATTENDANCE(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Default to current month and year if not provided
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
        except ValueError:
            return HttpResponse("Invalid month format.", status=400)
    else:
        today = datetime.today()
        year, month = today.year, today.month
    
    # Get the range of days in the selected month
    num_days = monthrange(year, month)[1]
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, num_days).date()
    
    try:
        # Fetch Attendance records for the selected date range and session_year
        attendance_instances = Attendance.objects.filter(
            attendance_date__range=(first_day, last_day),
            session_year_id=student.session_year.id
        )
        
        # Filter Attendance Reports for the student based on attendance instances
        attendance_records = Attendance_Report.objects.filter(
            student_id=student,
            attendance_id__in=attendance_instances
        ).select_related('attendance_id')

        # Calculate counts for the chart
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        leave_count = attendance_records.filter(status='leave').count()

    except Exception as e:
        return HttpResponse(f"Error fetching attendance records: {e}", status=500)

    # Convert attendance_records to a dictionary keyed by date
    attendance_dict = {
        record.attendance_id.attendance_date: record.status
        for record in attendance_records
    }
    
    # Prepare a list of all days in the month
    all_days_of_month = [first_day + timedelta(days=i) for i in range(num_days)]
    
    context = {
        'student': student,
        'attendance_records': attendance_dict,
        'all_days_of_month': all_days_of_month,
        'selected_month': month,
        'selected_year': year,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
    }
    
    return render(request, "Staff/staff_view_single_student_attendance.html", context)




# def VIEW_SINGLE_STUDENT_ATTENDANCE(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
    
#     # Default to current month and year if not provided
#     selected_month = request.GET.get('month')
#     if selected_month:
#         try:
#             month, year = map(int, selected_month.split('-'))
#         except ValueError:
#             # Handle invalid month format
#             return HttpResponse("Invalid month format.", status=400)
#     else:
#         today = datetime.today()
#         month, year = today.month, today.year
    
#     # Get the range of days in the selected month
#     num_days = monthrange(year, month)[1]
#     first_day = datetime(year, month, 1).date()
#     last_day = datetime(year, month, num_days).date()
    
#     # Filter Attendance records for the selected date range
#     try:
#         attendance_instances = Attendance.objects.filter(
#             attendance_date__range=(first_day, last_day)
#         )
#         attendance_records = Attendance_Report.objects.filter(
#             student_id=student,
#             attendance_id__in=attendance_instances
#         )
#     except Exception as e:
#         # Handle exceptions
#         return HttpResponse(f"Error fetching attendance records: {e}", status=500)

#     # Convert attendance_records to a dictionary keyed by date
#     attendance_dict = {
#         record.attendance_id.attendance_date: record
#         for record in attendance_records
#     }

#     # Calculate attendance statistics
#     present_count = attendance_records.filter(status='present').count()
#     absent_count = attendance_records.filter(status='absent').count()
#     leave_count = attendance_records.filter(status='leave').count()
    
#     # Prepare a list of all days in the month
#     all_days_of_month = [first_day + timedelta(days=i) for i in range(num_days)]
    
#     context = {
#         'student': student,
#         'attendance_records': attendance_dict,
#         'present_count': present_count,
#         'absent_count': absent_count,
#         'leave_count': leave_count,
#         'all_days_of_month': all_days_of_month,
#     }
    
#     # Render the response
#     return render(request, "Staff/staff_view_single_student_attendance.html", context)





