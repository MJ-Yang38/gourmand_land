import re
from django.shortcuts import redirect, render
from .models import User,Restaurant,Review
from django.contrib import messages
import bcrypt
from django.conf import settings

def index(request):
    return render(request,"index.html")
# register function here
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        if request.method=="POST":
            pword = request.POST['password']
            pw_hash = bcrypt.hashpw(pword.encode(), bcrypt.gensalt()).decode()  
            User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
        messages.success(request, "Successfully registered, now you can log in.")
        return redirect('/')
#login function here, first redirect then render a success page        
def login(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.filter(email=request.POST['user_email']) 
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        #indentation here is very important as only follows through if user[0] exists!!!!!!
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            #request.session['useremail'] = logged_user.email
            #request.session['userfirstname']=logged_user.first_name
            return redirect('/restaurants')
    #error message shows if login isn't successful        
    messages.error(request, "Login Failed!")
    return redirect('/')
#success page will be replaced by the wall page within just one app.#
#####################################################################
def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user
    }
    return render(request, 'restaurants.html', context)

#Have the logout link clear the session and redirect to the login/reg page
def logout(request):
    request.session.flush() #what's the difference between this and clear()?
    return redirect('/')


# Create your views here.
def createrestaurants(request):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Restaurant.objects.rest_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/restaurants')
    else:
        if request.method=="POST":
            Restaurant.objects.create(
                name=request.POST['name'],
                type=request.POST['type'],
                popular_items=request.POST['popular_items'],
                address=request.POST['address'],
                creater=User.objects.get(id=request.session['userid'])
            )
        return redirect('/restaurants/all')
#need to implement some methods to delete restaurants and reviews
#################################################################
def deleterest(request, rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method=='POST':
        this_rest=Restaurant.objects.get(id=rest_id)
        this_rest.delete()
        return redirect('/restaurants/all')

def all(request):
    if 'userid' not in request.session:
        return redirect('/')
    context={
        "all_restaurants":Restaurant.objects.all(),
        "user":User.objects.get(id=request.session['userid'])
    }
    return render(request,'restaurants_all.html',context)

def onerestaurant(request,rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    #figuring out the average rating of this restaurant    
    all_reviews=Review.objects.filter(reviewed_rest=Restaurant.objects.get(id=rest_id))
    rating_total=0
    total_num=Review.objects.filter(reviewed_rest=Restaurant.objects.get(id=rest_id)).count()
    if total_num!=0:
        for review in all_reviews:
            rating_total+=review.rating
        rating_avg=rating_total/(total_num)
    else:
        rating_avg=0
    rating_avg_int=int(rating_avg)

    context={
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        "rating_avg":rating_avg,
        "reviews":Review.objects.filter(reviewed_rest=Restaurant.objects.get(id=rest_id)),
        "user":User.objects.get(id=request.session['userid']),
        "this_rest":Restaurant.objects.get(id=rest_id),
        "rating_avg_int":rating_avg_int
    }
    return render(request,'one_restaurant.html',context)

#create reviews on 1 restaurant's page for that restaurant
############################
#################need to create a method to update the review and/or restaurant info
def createreview(request,rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Review.objects.rev_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/restaurants/{rest_id}')
    else:
        if request.method=="POST":
            Review.objects.create(
                rating=request.POST['rating'],
                content=request.POST['content'],
                reviewer=User.objects.get(id=request.session['userid']),
                reviewed_rest=Restaurant.objects.get(id=rest_id)
            )
        return redirect(f'/restaurants/{rest_id}')
#delete reviews left by user that's signed in 
def deletereview(request,review_id,rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method=="POST":
        this_review=Review.objects.get(id=review_id)
        this_review.delete()
        return redirect(f'/restaurants/{rest_id}')

def updatereviewpage(request,review_id,rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    context={
        "user":User.objects.get(id=request.session['userid']),
        "this_review": Review.objects.get(id=review_id),
        "this_rest": Restaurant.objects.get(id=rest_id)
    }
    return render(request,'updatereview.html',context)

def updatereview(request,review_id,rest_id):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Review.objects.rev_validator(request.POST)
    update_review=Review.objects.get(id=review_id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/restaurants/review/{rest_id}')
    else:
        if request.method=="POST":
            update_review.rating=request.POST['rating']
            update_review.content=request.POST['content']
            update_review.save()
        messages.success(request,"Review updated successfully!")
        return redirect(f'/restaurants/{rest_id}')
############################################
def oneuser(request,user_id):
    if 'userid' not in request.session:
        return redirect('/')
    this_user=User.objects.get(id=user_id)
    context={
        "this_user":this_user,
        
    }
    return render(request,'one_user.html',context)

def uploadimage(request,user_id):
    if 'userid' not in request.session:
        return redirect('/')
    this_user=User.objects.get(id=user_id)
    if request.method=="POST":
        this_user.image=request.FILES['image']
        this_user.save()
    return redirect(f'/restaurants/userprofile/{user_id}')

