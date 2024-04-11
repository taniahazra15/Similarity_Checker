import sys
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import*
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import DetailView
from difflib import SequenceMatcher
import aspose.words as aw
import fitz 
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import AssignmentUpload
import os
from django.http import JsonResponse
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import nltk
from difflib import SequenceMatcher
nltk.download('punkt')
nltk.download('stopwords')
# Create your views here.
def assignmnet_list(request):
    queryset = AddAssignment.objects.all()
    print(queryset)
    return render(request,'subject_list.html',{'queryset':queryset})

#Submitting Assignment
# def service_student(request):
#     if request.method == 'POST' and request.FILES.get('assignment'):
#         name = request.POST.get('name')
#         assignment_name = request.POST.get('assignment_name')
#         assignment = request.FILES['assignment']
        
#         # Create folder if it doesn't exist
#         folder_path = os.path.join('assignments', assignment_name)  # Relative path
#         os.makedirs(os.path.join('media', folder_path), exist_ok=True)
        
#         # Save the file to the folder
#         with open(os.path.join('media', folder_path, assignment.name), 'wb+') as destination:
#             for chunk in assignment.chunks():
#                 destination.write(chunk)
        
#         # Save the details to the database
#         assignment1 = AssignmentUpload.objects.create(
#             name=name,
#             folder_path=folder_path,
#             assignment_name=assignment_name,
#             assignment=os.path.join(folder_path, assignment.name),
#             user=request.user
#         )
        
#         return redirect('/service_student/')  # Redirect to a view showing the list of assignments
    
#     return render(request, 'service.html')




#check similarity and submit answer for student
def service_student(request):
    if request.method == 'POST' and request.FILES.get('assignment'):
        global alltext1, alltext2, str1, str2
        q1 = 0  
        alltext1 = ""
        alltext2 = ""
        str1 = ""
        str2 = ""
        q1 = 0
        flag = 0
        try:
            name = request.POST.get('name')
            assignment_name = request.POST.get('assignment_name')
            assignment = request.FILES['assignment']
            # Create folder if it doesn't exist
            folder_path = os.path.join('assignments', assignment_name) # Relative path
            os.makedirs(os.path.join('media', folder_path), exist_ok=True)
            # Save the file to the folder
            with open(os.path.join('media', folder_path, assignment.name), 'wb+') as destination:
                for chunk in assignment.chunks():
                    destination.write(chunk)
            
            action = request.POST.get('check')
            
            if action == 'press2':
                # Save the details to the database
                assignment1 = AssignmentUpload.objects.create(
                    name=name,
                    folder_path=folder_path,
                    assignment_name=assignment_name,
                    assignment=os.path.join(folder_path, assignment.name),
                    user=request.user
                )
                file_path1 = os.path.join('media', folder_path, assignment.name)
                str1 = alltext1
                print(file_path1)
                
                # Fetch folder path from AddAssignment based on assignmentName
                try:
                    add_assignment_record = AddAssignment.objects.get(assignmentName=assignment_name)
                    # root2 = add_assignment_record.folder_path1
                    filename2 = add_assignment_record.answer.name
                    print(filename2)
                    file_path2 = os.path.join('media', filename2)
                    print(file_path2)
                    
                    q1 = detect_plagiarism(file_path1, file_path2)
                    str2 = alltext2

                    print("q1 for press2=", q1)
                    return render(request, "service.html", {"output": q1})
                except AddAssignment.DoesNotExist:
                    # Handle the case where there's no matching assignmentName in AddAssignment
                    pass
                
            elif action == 'press1':
                # Save the details to the database
                assignment1 = AssignmentUpload.objects.create(
                    name=name,
                    folder_path=folder_path,
                    assignment_name=assignment_name,
                    assignment=os.path.join(folder_path, assignment.name),
                    user=request.user
                )

                print("q1 for press1=", q1)
                
                return render(request, "service.html")
                 
        except Exception as e:
            print(e)
    
    return render(request, 'service.html')

#check similarity percentage for teacher
def check_similarity(request):
    if request.method == 'POST':
        global alltext1,alltext2,str1,str2
        q1=0  
        alltext1=""
        alltext2=""
        str1=""
        str2=""
        q1=0
        flag=0
        try:
                   assignment_link = request.POST.get('assignment_link')
                   assignment_link1=request.POST.get('assignment_link1')
                   action=request.POST.get('check')
                   
                   if (action=='press2'):
                                 file_path1=os.path.join('media',assignment_link)
                                 str1=alltext1
                                 print(file_path1)
              

                                #  root2="C:\\Users\\hazra\\env\\FinalYear\\media\\Answer"
                                # #  filename2="Text1.pdf"
                                #  filename2="Tania.pdf"

                                 file_path2=os.path.join('media',assignment_link1)
                                 str2=alltext2
                               
                                 q1=detect_plagiarism(file_path1, file_path2)
                                 

                               
                                 print("q1 for press2=",q1)
                                 return render(request,"check_similarity.html",{"output":q1})
                
                                 
                                
                 
        except:
             pass
        
    
    return render(request, 'check_similarity.html')


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
            print(text)
    return text


def detect_plagiarism(file_path1, file_path2):
    # Extract text from PDF files
    assignment1_text = extract_text_from_pdf(file_path1)
    assignment2_text = extract_text_from_pdf(file_path2)
    
    # Preprocess text
    assignment1_text_processed = preprocess_text(assignment1_text)
    assignment2_text_processed = preprocess_text(assignment2_text)
    
    # Compute similarity matrix
    similarity_matrix = compute_similarity_matrix([assignment1_text_processed, assignment2_text_processed])
    
    # Output the result
    print("Similarity percentage:", similarity_matrix[0][1] * 100)
    final_result=similarity_matrix[0][1] * 100
    return  final_result

def compute_similarity_matrix(assignments):
          tfidf_vectorizer = TfidfVectorizer()
          tfidf_matrix = tfidf_vectorizer.fit_transform(assignments)
          similarity_matrix = cosine_similarity(tfidf_matrix)
          print("vectorization is successful")
          return similarity_matrix
    


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters and extra whitespaces
    text = re.sub(r'\W+', ' ', text)
    # Tokenization
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    # Convert tokens back to text
    processed_text = ' '.join(tokens)
    print("preprocess is successful")
    print("after preprocess text is:-", processed_text)
    return processed_text
    
def service_admin(request):
    return render(request,"service1.html")

#For Adding Assignment
def add_assignmnet(request):
    if request.method == "POST" and request.FILES.get('answer'):
        username = request.POST.get('username')
        # folder_path1= os.path.join('Answer', assignment_name)
        assignment_name = request.POST.get('assignmentName')
        assignment_file = request.POST.get('assignment_file')
        answer = request.FILES.get("answer")

        # Create folder if it doesn't exist
        folder_path1 = os.path.join('Answer', assignment_name)  # Relative path
        os.makedirs(os.path.join('media', folder_path1), exist_ok=True)

        # Save the file to the folder
        with open(os.path.join('media', folder_path1, answer.name), 'wb+') as destination:
            for chunk in answer.chunks():
                destination.write(chunk)

        # Save the assignment details to the database
        assignment = AddAssignment.objects.create(
            username=username,
            folder_path1=folder_path1,
            assignmentName=assignment_name,
            assignment_file=assignment_file,
            answer=os.path.join(folder_path1, answer.name),
            user=request.user
        )
        
        messages.info(request, 'Assignment added successfully')
        return redirect('/add_assignmnet/')
    
    return render(request, 'add_assignmnet.html')
#Search For Assignment for teachers
def Search_classname(request):
    if request.method=="POST":
        search_classname=request.POST.get('search_classname')
        messages.info(request,'Your result')
        queryset=AddAssignment.objects.all()
        print(queryset)
        if search_classname:
            queryset = queryset.filter(username=search_classname)
        return render(request, 'search_assignment.html', {'queryset': queryset})

    return render(request,'search_assignment.html')
#search for answer PDF
def Search_answers(request):
    if request.method=="POST":
        search_assignmentname=request.POST.get('search_assignmentname')
        messages.info(request,'Your result')
        queryset=AssignmentUpload.objects.all()
        print(queryset)
        if search_assignmentname:
            queryset = queryset.filter(assignment_name=search_assignmentname)
        return render(request, 'search_answer.html', {'queryset': queryset})

    return render(request,'search_answer.html')

def Search_classname_student(request):
    if request.method=="POST":
        search_classname_student=request.POST.get('search_classname_student')
        messages.info(request,'Your result')
        queryset=AddAssignment.objects.all()
        print(queryset)
        if search_classname_student:
            queryset = queryset.filter(username=search_classname_student)
        return render(request, 'search_upcoming_assignment.html', {'queryset': queryset})

    return render(request,'search_upcoming_assignment.html')


def add_course(request):
    if request.method == "POST":
        username=request.POST.get('username')
        classcode=request.POST.get('classcode')
        section=request.POST.get('section')
        room_number=request.POST.get('room_number')
        subject=request.POST.get('subject')
        #for saving the model
        user=AddCourse.objects.filter(classcode=classcode)
        if user.exists():
            messages.info(request,'Coursename exists')
            return redirect('/add_course/')
        #getting data
        user=AddCourse.objects.create(
            username=username,
            classcode=classcode,
            section=section,
            room_number=room_number,
            subject=subject,
            user=request.user
        )
        messages.info(request,'Course added successfully')
        return redirect('/add_course/')
    queryset = AddCourse.objects.filter(user=request.user)
    print(queryset)
    
    return render(request,'add_course.html',{'queryset':queryset})

def student_home(request):
    return render(request,'student_home.html')

def student_pannel(request):
    
    string_arr=[]
    if request.method == "POST":
        username=request.POST.get('username')
        classcode=request.POST.get('classcode')
        
        if  AddCourse.objects.filter(classcode=classcode).exists():
            user=StudentPannel.objects.create(
            username=username,
            classcode=classcode,
            user=request.user,
            )
            messages.info(request,'Course added successfully')
            # sys.exit()
            return redirect('/student_pannel/')
        
            
        else:
            messages.error(request,'Invalid code')
            return redirect('/student_pannel/')
            
        
    querysett=StudentPannel.objects.filter(user=request.user)
    print(querysett)
    
        
    return render(request,'student_main.html',{'querysett':querysett})
    







