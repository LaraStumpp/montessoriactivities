from django.shortcuts import render, redirect
from .models import User, Activity, Category, Comment
from django.contrib import messages
from .forms import *
import bcrypt
from django.core.files.storage import FileSystemStorage
#from .models import Quote
#from loginAndRegistration_app.models import User
#from django.contrib import messages
#from datetime import datetime, timezone

def index(request):
    categories=Category.objects.all()
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])

    practicalLifeCat = Category.objects.filter(name='Practical Life ')[0]
    math = Category.objects.filter(name='Mathematics')[0]
    language = Category.objects.filter(name='Language')[0]
    culturalStudies = Category.objects.filter(name='Cultural Studies')[0]

    context = {
        "categoriesForHtml": categories,
        "userForHtml":user,
        "practicalLifeCat": practicalLifeCat,
        "math":math,
        "language":language,
        "culturalStudies": culturalStudies
    }

    return render(request,'index.html', context)

def showDashboard(request):
    activities=Activity.objects.all()
    categories=Category.objects.all()
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        
    if user == None or user.isAdmin == False:
        return redirect('/')

    context = {
        "activitiesForHtml": activities,
        "categoriesForHtml": categories,
        "userForHtml":user
    }
    return render(request, 'dashboard_admin.html', context)

def showAddActivity(request):
    activities=Activity.objects.all()
    categories=Category.objects.all()
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        
    if user == None or user.isAdmin == False:
        return redirect('/')

    context = {
        "activitiesForHtml": activities,
        "categoriesForHtml": categories,
         "userForHtml":user
    }

    return render(request, 'dashboard_add_activity.html',context)


def showRegister(request):
    categories=Category.objects.all()
    context = {
        "categoriesForHtml": categories
    }
    return render(request,'register.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)

        userCount=User.objects.all().count()
        if userCount == 0:
            user=User.objects.create(fname=request.POST['fname'], email=request.POST['email'], password=pw_hash, isAdmin=True)
            print("Admin erstellt!")
        else:
            user=User.objects.create(fname=request.POST['fname'], email=request.POST['email'], password=pw_hash, isAdmin=False)
            print("User erstellt!")

        request.session['userId'] = user.id
        request.session['fname'] = user.fname

        return redirect('/')

def showLogin(request):
    categories=Category.objects.all()
    context = {
        "categoriesForHtml": categories
    }

    return render(request,'login.html', context)

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userId'] = logged_user.id
            request.session['fname'] = logged_user.fname
            return redirect('/')
    return redirect('/login')

def logout(request):
    del request.session['userId']
    del request.session['fname']
    return redirect('/')

# Creates and stores a new activity in the system
def createActivity(request):
    
    # Do input validation
    errors = Activity.objects.activity_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/admin/add/')
    else:
        # Make sure user is admin
        user = None
        if 'userId' in request.session:
            user = User.objects.get(id=request.session['userId'])
        
        # Do not allow non-admins or non-signed in users to upload content
        if user == None or user.isAdmin == False:
            return redirect('/')

        # Upload image and store in file system storage
        myfile= request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        url = fs.url(filename)

        # Upload pdf and store in file system storage
        pdfUrl = None
        if 'mypdf' in request.FILES:
            mypdf= request.FILES['mypdf']
            fs = FileSystemStorage()
            filename = fs.save(mypdf.name, mypdf)
            pdfUrl = fs.url(filename)

        # Check whether we need to create a new category or use an existing one
        if(request.POST['addNewCategory'] != ''):
            category= Category.objects.create(
                name=request.POST['addNewCategory']
                )

            activity= Activity.objects.create(
                    title=request.POST['title'],
                    age=request.POST['age'],
                    content=request.POST['content'],
                    category=category,
                    title_image_url=url,
                    document_url=pdfUrl
                    )
        else:
            category=Category.objects.get(id=request.POST['category'])

            activity= Activity.objects.create(
                    title=request.POST['title'],
                    age=request.POST['age'],
                    content=request.POST['content'],
                    category=category,
                    title_image_url=url,
                    document_url=pdfUrl
                    )
            print("Activity erstellt!!!!!!!!!!!!")
        return redirect('/dashboard/admin')

def showActivities(request):
    activities = Activity.objects.all()
    categories=Category.objects.all()
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])

    if 'categoryId' in request.GET:
        category = Category.objects.get(id=request.GET.get('categoryId'))
        activities=activities.filter(category=category)

    if 'age' in request.GET:
        activities = activities.filter(age=request.GET['age'])

    if 'keyword' in request.GET:
        activities = activities.filter(content__contains=request.GET['keyword'])
    
    context = {
        "activitiesForHtml": activities,
        "categoriesForHtml": categories,
        "userForHtml":user
    }

    return render(request,'activities.html', context)


def showActivity(request, activity_id):
    activity=Activity.objects.get(id=activity_id)
    categories=Category.objects.all()
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])


    context={
        "activityForHtml": activity,
        "categoriesForHtml": categories,
        "userForHtml":user
    }
    return render(request,'activity-single.html', context)



def activitiesFilter(request):
    parameterList= ""
    
    if request.POST['categoryId'] != '':
        parameterList = parameterList + 'categoryId=' + request.POST['categoryId'] +'&'
        
    if request.POST['age'] != '':
        parameterList = parameterList + 'age=' + request.POST['age'] + '&'
    
    if request.POST['keyword'] !='':
        parameterList= parameterList + 'keyword=' + request.POST['keyword']

    return redirect('/activities?' + parameterList)
    

def editActivity(request, activity_id):
    
    activity=Activity.objects.get(id=activity_id)
    categories=Category.objects.all()
    
    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        
    if user == None or user.isAdmin == False:
        return redirect('/')

    context={
        "activityForHtml": activity,
        "categoriesForHtml": categories,
        "userForHtml":user
    }

    return render(request,'dashboard_edit_activity.html', context)


def saveActivity(request, activity_id):

    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        
    if user == None or user.isAdmin == False:
        return redirect('/')

    category=Category.objects.get(id=request.POST['category'])

    activity= Activity.objects.get(id=activity_id)
    activity.title=request.POST['title']
    activity.age=request.POST['age']
    activity.category =category
    activity.content=request.POST['content']
   
    activity.save()

    return redirect('/dashboard/admin')


def deleteActivity(request, activity_id):

    user = None
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        
    if user == None or user.isAdmin == False:
        return redirect('/')

    activity= Activity.objects.get(id=activity_id)
    activity.delete()


    return redirect('/dashboard/admin')


def createComment(request, activity_id):
    activity= Activity.objects.get(id=activity_id)
    user = User.objects.get(id=request.session['userId'])
    comment= Comment.objects.create(
                comment=request.POST['comment'],
                activity=activity,
                user=user
                )


    return redirect('/activity/' + str(activity.id))
