from django.db import models

# Create your models here.

class Genders(models.Model):
    class Meta:
        db_table = 'tbl_genders'

    gender_id = models.BigAutoField(primary_key=True, blank=False) # gender_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY
    gender = models.CharField(max_length=55, blank=False) # gender VARCHAR(55) NOT NULL
    created_at = models.DateTimeField(auto_now_add=True) # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True) # updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

class Users(models.Model):
    class Meta:
        db_table = 'tbl_users'

    user_id = models.BigAutoField(primary_key=True, blank=False) # user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY
    full_name = models.CharField(max_length=55, blank=False) # full_name VARCHAR(55) NOT NULL
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE) # gender_id BIGINT NOT NULL // FOREGN KEY(gender_id) REFERENCES tbl gender(gender_id) ON DELETE CASCADE
    birth_date = models.DateField(blank=False) # birth_date DATE NOT NULL
    address = models.CharField(max_length=255, blank=False) # address VARCHAR(255) NOT NULL
    contact_number = models.CharField(max_length=55, blank=False) # contact_number VARCHAR(55) NOT NULL
    email = models.CharField(max_length=55, blank=True) # email VARCHAR(55) DEFAULT NULL
    username = models.CharField(max_length=55, blank=False, unique=True) # username VARCHAR(55) NOT NULL UNIQUE
    password = models.CharField(max_length=255, blank=False) # password VARCHAR(255) NOT NULL
    created_at = models.DateTimeField(auto_now_add=True) # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at = models.DateTimeField(auto_now=True) # updated_at TIMESTAMP DEFAULT CURRENT

# restaurant ini

class Dashboard(models.Model):
    
    pass

class MenuItems(models.Model):
    menu_item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    table_id = models.IntegerField(null=True, blank=True) 
    status = models.CharField(max_length=50, default='PLACED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.status}"

class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    notes = models.TextField(null=True, blank=True)

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    table_id = models.IntegerField(null=True, blank=True) 
    reservation_time = models.DateTimeField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=50, default='PENDING')

class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='PAID')
    paid_at = models.DateTimeField(null=True, blank=True)   