from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if str.isalpha(postData['first_name'])==False:
            errors["first_name_letters"] = "First name should be letters only"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if str.isalpha(postData['last_name'])==False:
            errors["last_name_letters"] = "Last name should be letters only"
        #checking email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']): # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")  
        #checking the uniqueness of the email address
        this_email=User.objects.filter(email=postData['email'])
        if len(this_email)>0:
            errors['unique_email']="This email already exists!" 
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"
        #check if passwords are matching
        if postData['confirm_pw']!=postData['password']:
            errors['pw']="Passwords aren't matching!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    image=models.ImageField(default="default.jpeg", blank=True)#adding image field for uploading images
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    #list of restaurants_entered 
    #list of user_reviews
class RestaurantManager(models.Manager):
    def rest_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Restaurant name should be at least 2 characters."
        if len(postData['type']) < 2:
            errors["type"] = "Restaurant type should be at least 2 characters." 
        if len(postData['popular_items']) < 5:
            errors["popular_items"] = "Popular items should be at least 5 characters."
        return errors
class Restaurant(models.Model):
    name=models.CharField(max_length=255)
    type=models.CharField(max_length=45)
    popular_items=models.TextField()
    address=models.CharField(max_length=255)
    creater=models.ForeignKey(User, related_name="restaurants_entered", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=RestaurantManager()
    #list of rest_reviews

class ReviewManager(models.Manager):
    def rev_validator(self, postData):
        errors = {}
        if postData['rating']=='': 
            errors["rating2"]="Please enter review rating."
        elif int(float(postData['rating']))< 0 or int(float(postData['rating']))>5:#this will break if empty rating so changing if to elif here fixed it.
            errors["rating"] = "Review rating should be a whole number between 0-5."
        if len(postData['content']) < 8:
            errors["content"] = "Review content should be at least 8 characters." 
        return errors
class Review(models.Model):
    rating=models.IntegerField()
    content=models.TextField()
    reviewer=models.ForeignKey(User, related_name="user_reviews", on_delete = models.CASCADE)
    reviewed_rest=models.ForeignKey(Restaurant, related_name="rest_reviews", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ReviewManager()