from django.db import models


class Role(models.Model):
    role_id   = models.AutoField(primary_key=True, db_column='role_id')
    role_name = models.CharField(max_length=50, db_column='role_name')

    class Meta:
        managed = False
        db_table = 'Roles'

    def __str__(self):
        return self.role_name


class User(models.Model):
    user_id    = models.AutoField(primary_key=True, db_column='user_id')
    surname    = models.CharField(max_length=60, db_column='surname')
    name       = models.CharField(max_length=60, db_column='name')
    patronymic = models.CharField(max_length=60, null=True, blank=True, db_column='patronymic')
    login      = models.CharField(max_length=40, unique=True, db_column='login')
    password   = models.CharField(max_length=120, db_column='password')
    role       = models.ForeignKey(Role, on_delete=models.PROTECT, db_column='role_id')

    class Meta:
        managed = False
        db_table = 'Users'

    @property
    def full_name(self):
        return f'{self.surname} {self.name[:1]}.{(self.patronymic or "")[:1]}.'.strip('.')


class Category(models.Model):
    category_id   = models.AutoField(primary_key=True, db_column='category_id')
    category_name = models.CharField(max_length=80, db_column='category_name')

    class Meta:
        managed = False
        db_table = 'Categories'

    def __str__(self):
        return self.category_name


class Manufacturer(models.Model):
    manufacture_id   = models.AutoField(primary_key=True, db_column='manufacture_id')
    manufacture_name = models.CharField(max_length=80, db_column='manufacture_name')

    class Meta:
        managed = False
        db_table = 'Manufactures'

    def __str__(self):
        return self.manufacture_name


class Supplier(models.Model):
    suplyer_id   = models.AutoField(primary_key=True, db_column='suplyer_id')
    suplyer_name = models.CharField(max_length=120, db_column='suplyer_name')
    inn          = models.CharField(max_length=12, db_column='inn')
    address      = models.CharField(max_length=200, null=True, blank=True, db_column='address')

    class Meta:
        managed = False
        db_table = 'Suplyers'

    def __str__(self):
        return self.suplyer_name


class Product(models.Model):
    article        = models.CharField(primary_key=True, max_length=20, db_column='article')
    name           = models.CharField(max_length=150, db_column='name')
    unit           = models.CharField(max_length=20, null=True, blank=True, db_column='unit')
    price          = models.DecimalField(max_digits=12, decimal_places=2, db_column='price')
    max_discount   = models.IntegerField(null=True, blank=True, db_column='max_discount')
    manufacture    = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, null=True, db_column='manufacture_id')
    suplyer        = models.ForeignKey(Supplier,     on_delete=models.PROTECT, null=True, db_column='suplyer_id')
    category       = models.ForeignKey(Category,     on_delete=models.PROTECT, null=True, db_column='category_id')
    discount       = models.IntegerField(default=0,  db_column='discount')
    quantity       = models.IntegerField(default=0,  db_column='quantity')
    description    = models.TextField(null=True, blank=True, db_column='description')
    image_path     = models.CharField(max_length=255, null=True, blank=True, db_column='image_path')

    class Meta:
        managed = False
        db_table = 'Products'

    @property
    def final_price(self):
        return round(float(self.price) * (100 - (self.discount or 0)) / 100, 2)

    @property
    def is_highlighted(self):
        return (self.discount or 0) > 12

    @property
    def out_of_stock(self):
        return (self.quantity or 0) == 0


class PickPoint(models.Model):
    pickpoint_id = models.AutoField(primary_key=True, db_column='pickpoint_id')
    address      = models.CharField(max_length=200, db_column='address')

    class Meta:
        managed = False
        db_table = 'PickPoints'

    def __str__(self):
        return self.address


class Order(models.Model):
    order_id      = models.AutoField(primary_key=True, db_column='order_id')
    pickpoint     = models.ForeignKey(PickPoint, on_delete=models.PROTECT, null=True, db_column='pickpoint_id')
    order_date    = models.DateField(db_column='order_date')
    delivery_date = models.DateField(null=True, blank=True, db_column='delivery_date')
    status        = models.CharField(max_length=30, default='Новый', db_column='status')
    user          = models.ForeignKey(User,     on_delete=models.PROTECT, null=True, db_column='user_id')
    product       = models.ForeignKey(Product,  on_delete=models.PROTECT, null=True, db_column='article')
    quantity      = models.IntegerField(default=1, db_column='quantity')
    pickup_code   = models.IntegerField(null=True, blank=True, db_column='pickup_code')

    class Meta:
        managed = False
        db_table = 'Orders'
