from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users, Dashboard, Reservations, MenuItems, Orders, OrderItems, Bills
from django.contrib.auth.hashers import make_password
from django.utils import timezone
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
        return render(request, 'management/indexmanage.html')
    except Exception as e:
        return HttpResponse(f'Error: {e}')
    
def order_list(request):
    try:
        return render(request, 'order/OrdersList.html', {'orders': Orders.objects.select_related('user').all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def add_order(request):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=request.POST.get('user_id'))
            tableId = request.POST.get('table_id')
            Orders.objects.create(user=userObj, table_id=tableId if tableId else None, status='PLACED')
            messages.success(request, 'Order opened successfully!')
            return redirect('/order/list')
        return render(request, 'order/AddOrder.html', {'users': Users.objects.all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def order_detail(request, orderId):
    try:
        order = get_object_or_404(Orders, pk=orderId)
        items = OrderItems.objects.filter(order=order).select_related('menu_item')
        return render(request, 'order/OrderDetail.html', {'order': order, 'items': items})
    except Exception as e:
        return HttpResponse(f'Error: {e}')
    
def add_order_item(request, orderId):
    try:
        orderObj = get_object_or_404(Orders, pk=orderId)
        if request.method == 'POST':
            menuItemObj = MenuItems.objects.get(pk=request.POST.get('menu_item_id'))
            OrderItems.objects.create(
                order=orderObj,
                menu_item=menuItemObj,
                quantity=int(request.POST.get('quantity', 1)),
                notes=request.POST.get('notes', '')
            )
            messages.success(request, f'Added {menuItemObj.name} to Order #{orderId}')
            return redirect(f'/order/detail/{orderId}')
        return render(request, 'order/AddOrderItem.html', {'order': orderObj, 'menu_items': MenuItems.objects.filter(is_available=True)})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def update_order_status(request, orderId):
    try:
        orderObj = get_object_or_404(Orders, pk=orderId)
        if request.method == 'POST':
            orderObj.status = request.POST.get('status')
            orderObj.save()
            messages.success(request, f'Order #{orderId} status updated successfully.')
            return redirect(f'/order/detail/{orderId}')
        return render(request, 'order/UpdateOrderStatus.html', {'order': orderObj})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def delete_order(request, orderId):
    try:
        orderObj = get_object_or_404(Orders, pk=orderId)
        if request.method == 'POST':
            orderObj.delete()
            messages.success(request, f'Order #{orderId} was successfully deleted.')
            return redirect('/order/list')
        return render(request, 'order/DeleteOrderConfirm.html', {'order': orderObj})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def reservation_list(request):
    try:
        return render(request, 'reservation/ReservationsList.html', {'reservations': Reservations.objects.select_related('user').all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def add_reservation(request):
    try:
        if request.method == 'POST':
            Reservations.objects.create(
                table_id=request.POST.get('table_id'),
                user=get_object_or_404(Users, pk=request.POST.get('user_id')),
                reservation_time=request.POST.get('reservation_time'),
                number_of_guests=request.POST.get('number_of_guests'),
                status='PENDING'
            )
            messages.success(request, 'Reservation booked successfully!')
            return redirect('/reservation/list')
        return render(request, 'reservation/AddReservation.html', {'users': Users.objects.all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def edit_reservation(request, reservationId):
    try:
        resObj = get_object_or_404(Reservations, pk=reservationId)
        if request.method == 'POST':
            resObj.table_id = request.POST.get('table_id')
            resObj.user = Users.objects.get(pk=request.POST.get('user_id'))
            resObj.reservation_time = request.POST.get('reservation_time')
            resObj.number_of_guests = request.POST.get('number_of_guests')
            resObj.status = request.POST.get('status')
            resObj.save()
            messages.success(request, 'Reservation updated successfully!')
            return redirect('/reservation/list')
        return render(request, 'reservation/EditReservation.html', {'reservation': resObj, 'users': Users.objects.all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def delete_reservation(request, reservationId):
    try:
        resObj = get_object_or_404(Reservations, pk=reservationId)
        if request.method == 'POST':
            resObj.delete()
            messages.success(request, 'Reservation deleted successfully!')
            return redirect('/reservation/list')
        return render(request, 'reservation/DeleteReservation.html', {'reservation': resObj})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def bill_list(request):
    try:
        return render(request, 'bill/BillsList.html', {'bills': Bills.objects.select_related('order').all()})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def bill_detail(request, billId):
    try:
        billObj = Bills.objects.select_related('order__user').get(pk=billId)
        items = OrderItems.objects.filter(order=billObj.order).select_related('menu_item')
        return render(request, 'bill/BillDetail.html', {'bill': billObj, 'order_items': items})
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def process_payment(request, billId):
    try:
        orderObj = get_object_or_404(Orders, pk=billId)
        orderItems = OrderItems.objects.filter(order=orderObj).select_related('menu_item')
        
        if not orderItems.exists():
            return HttpResponse("Cannot checkout an empty order.", status=400)

        subtotal = sum(item.quantity * item.menu_item.price for item in orderItems)
        tax_amount = subtotal * Decimal('0.12')
        grand_total = subtotal + tax_amount

        if request.method == 'POST':
            billObj = Bills.objects.create(
                order=orderObj,
                total_amount=subtotal,
                tax=tax_amount,
                discount=Decimal('0.00'),
                final_amount=grand_total,
                payment_method=request.POST.get('payment_method'),
                status='PAID',
                paid_at=timezone.now()
            )
            orderObj.status = 'COMPLETED'
            orderObj.save()
            messages.success(request, f'Bill #{billObj.bill_id} paid successfully!')
            return redirect('/bill/list')
            
        data = {
            'order': orderObj,
            'orderItems': orderItems,
            'subtotal': subtotal,
            'tax': tax_amount,
            'grand_total': grand_total,
        }
        return render(request, 'bill/ProcessPayment.html', data)
    except Exception as e:
        return HttpResponse(f'Error: {e}')