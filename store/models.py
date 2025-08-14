from django.db import models 
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#Create customer Profile
class Profile(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   data_modified=models.DateTimeField(auto_now=True)
   phone=models.CharField(max_length=12,blank=True)
   address1=models.CharField(max_length=200,blank=True)
   address2=models.CharField(max_length=200,blank=True)
   city=models.CharField(max_length=200,blank=True)
   state=models.CharField(max_length=200,blank=True)
   zipcode=models.CharField(max_length=200,blank=True)
   country=models.CharField(max_length=200,blank=True)
   old_cart=models.TextField(max_length=200,blank=True,null=True)

   def __str__(self):
      return self.user.username
#Create  a user  Profile  by default when user signs up 
def create_profile(sender,instance,created,**kwargs):
   if created:
      user_profile=Profile(user=instance)
      user_profile.save()
      
post_save.connect(create_profile,sender=User)
class Category(models.Model):

    name =models.CharField(max_length=155, db_index=True)

    slug =models.SlugField(max_length=155,unique=True) 
    
    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural='categories'
 

    
    
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=100)

    def _str_(self):
     return self.name
    
    class Meta:
     verbose_name_plural ='customer'




CATEGORY_CHOICES=(

    ('C','Computer'),
    ('M','Mobile'),
    ('T','Tablet')
)

LABEL_CHOICES=(
    ('N','New'),
    ('R','Refurbished'),
    ('U','Used')

)
class Items(models.Model):

    title = models.CharField(max_length=155)

    brand = models.CharField(max_length=155,default='un-branded')

    description = models.TextField(blank=True)

    slug=models.SlugField(max_length=155)

    price = models.DecimalField(default=0,max_digits=5,decimal_places=2)

    image = models.ImageField(upload_to='images/') 

    discount_price = models.FloatField()

    category=models.CharField(choices=CATEGORY_CHOICES,max_length=5)

    label=models.CharField(choices=LABEL_CHOICES,max_length=5)
    is_sale=models.BooleanField(default=False)
    sale_price= models.DecimalField(default=0 ,max_digits=5,decimal_places=2)
    def _str_(self):
      return self.name

    class Meta:
     verbose_name_plural ='products '



class Order(models.Model):
    product=models.ForeignKey(Items,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=122,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    def _str_(self):
     return self.name
    class Meta:
     verbose_name_plural ='Orders '

def get_discount_percent(self):
    discount_percent=100-(self.dicount_price*100/ self.price)
    return discount_percent


def get_item_url(self):
    return reverse('frontend: detail',kwargs={
        'slug':self.slug
    })