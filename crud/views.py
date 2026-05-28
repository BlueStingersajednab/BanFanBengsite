from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from crud.models import (MenuItems)
from django.db.models import Sum, Avg
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from decimal import Decimal

def gender_list(request):
  try:
     genders = Genders.objects.all() # SELECT * FROM tbl_genders;

     data = {
        'genders':genders # data
     }
      
     return render(request, 'gender/GendersList.html', data)
  except Exception as e:
     return HttpResponse(f'Error occurred during load genders: {e}')

def add_gender(request):
  try:
      if request.method == 'POST':  
        gender = request.POST.get('gender')

        Genders.objects.create(gender=gender).save() # INSERT INTO tbl_genders(gender) VALUES(gender);
        messages.success(request, 'Gender added successfully!')
        return redirect ('/gender/list')
      else:
        return render(request, 'gender/AddGender.html')
  except Exception as e:
     return HttpResponse(f'Error occurred during add gender: {e}')

def edit_gender(request, genderId):
   try:
      if request.method == 'POST':
         genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;

         gender = request.POST.get('gender')

         genderObj.gender = gender
         genderObj.save() # UPDATE tbl_genders SET gender = gender WHERE gender_id = genderId;

         messages.success(request, 'Gender updated successfully!')

         data = {
          'gender':genderObj
        }
         
         return render(request, 'gender/EditGender.html', data)
      else:
         genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;

         data = {
           'gender':genderObj
        }

      return render(request, 'gender/EditGender.html', data)
   
   except Exception as e:
     return HttpResponse(f'Error occurred during edit gender: {e}')

def delete_gender(request, genderId):
   try:
      if request.method == 'POST':
        genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;
        genderObj.delete() #DELETE FROM tbl_genders WHERE gender_id = genderId;

        messages.success(request, 'Gender deleted successfully!')
        return redirect('/gender/list')
      else:
        genderObj = Genders.objects.get(pk=genderId) # SELECT * FROM tbl_genders WHERE id = genderId;

        data = {
          'gender':genderObj
        }

        return render(request, 'gender/DeleteGender.html', data)
   except Exception as e:
      return HttpResponse(f'Error occurred during delete gender: {e}')
   
def user_list(request):
   try:
      userObj = Users.objects.select_related('gender') # SELECT * FROM tbl_users INNER JOIN tb_genders ON tbl_users.gender_id = tbl.genders,gender_id ;

      data ={
         'users': userObj
      }

      return render(request, 'user/UsersList.html', data)
   except Exception as e:
      return HttpResponse(f'Error Occurred during load users: {e}')


def add_user(request):
   try:
      if request.method == 'POST':
         fullName = request.POST.get('full_name')
         gender = request.POST.get('gender')
         birthDate = request.POST.get('birth_date')
         address = request.POST.get('address')
         contactNumber = request.POST.get('contact_number')
         email = request.POST.get('email')
         username = request.POST.get('username')
         password = request.POST.get('password')
         confirmPassword = request.POST.get('confirm_Password')

         #if password != confirmPassword:
         # show an error if password is wrong

         Users.objects.create(
            full_name=fullName,
            gender=Genders.objects.get(pk=gender), 
            birth_date=birthDate,
            address=address,
            contact_number=contactNumber,
            email=email,
            username=username,
            password=make_password(password) #Hash the password before saving it
         ).save() # INSERT INTO tbl_users(full_name, gender_id, birth_date, address, contact_number, email, username, password) VALUES
         #(fullName, gender, birthdate, address, contactNumber, email, username, password);
         messages.success(request, 'User added successfully!')
         return redirect('/user/add')
      else:
         genderObj = Genders.objects.all() # SELECT * FROM tbl_genders;

         data = {
            'genders': genderObj
         }

         return render(request, 'user/AddUser.html', data)
   except Exception as e:
      return HttpResponse(f'Error occurred during add user: {e}')  
   
   # other project sa management diri

def dashboard_home(request):

    try:
#  test lang muna
        data = {               
            'today_revenue': 0,
            'today_orders': 0,
            'avg_expense': 0,
            'avg_revenue': 0,
        }

        return render(
            request,
            'management/indexmanage.html',
            data
        )

    except Exception as e:
        return HttpResponse(f'Error: {e}')
# TESTT

def menu_list(request):
    menu_items = MenuItems.objects.all()
    return render(request, "management/foodmenu.html", {"menu_items": menu_items})


def add_menu_item(request):
    if request.method == "POST":
        MenuItems.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            description=request.POST.get("description")
        )
    return redirect("menu_list")


def edit_menu_item(request, id):
    item = get_object_or_404(MenuItems, id=id)

    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.save()
        return redirect("menu_list")

    return render(request, "edit_menu.html", {"item": item})


def delete_menu_item(request, id):
    item = get_object_or_404(MenuItems, id=id)
    item.delete()
    return redirect("menu_list")

