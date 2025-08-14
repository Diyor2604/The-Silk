from store.models import Items,Profile
class Cart:
    def __init__(self,request):
      self.session=request.session

      self.request=request
      #Get the current session key if it exists
      cart=self.session.get('session_key')
      #If the user is new ,no session key!Create one!
      if 'session_key' not in request.session:
         cart=self.session['session_key']={}

      #Make sure cart is available on all ages of site
      self.cart=cart 
    def db_add(self,product,quantity):
       product_id=str(product )
       product_qty=str(product)
        #Logic
       if product_id in self.cart:
        pass
       else:
        #self.cart[product_id]={'price':str(product.price)}
         self.cart[product_id]=int(product_qty)
       self.session.modified=True
       #Deal with logged in user
       if self.request.user.is_authenticated:
        #Get the current user Profile
        current_user=Profile.objects.filter(user__id=self.request.user.id)
        #Convert {'3':1,'2':4} to {"3":1,"2":4 }
        carty=str(self.cart)
        carty=carty.replace("\'","\"")
        #Save the carty to Profile Model
        current_user.update(old_cart=str(carty))
    
    def add(self,product):
     product_id=str(product_id )
     product_qty=str(product_qty)
     #Logic
     if product_id in self.cart:
        pass
     else:
        #self.cart[product_id]={'price':str(product.price)}
         self.cart[product_id]=int(product_qty)
     self.session.modified=True
       #Deal with logged in user
     if self.request.user.is_authenticated:
        #Get the current user Profile
        current_user=Profile.objects.filter(user__id=self.request.user.id)
        #Convert {'3':1,'2':4} to {"3":1,"2":4 }
        carty=str(self.cart)
        carty=carty.replace("\'","\"")
        #Save the carty to Profile Model
        current_user.update(old_cart=str(carty))
 
    def cart_total(self):
       
       #Get product IDS
       product_ids=self.cart.keys()
       products=Items.objects.filter(id__in=product_ids)
       {'4':3,'2':5}
       quantities=self.cart
       #Start countingat 0
       total=0
       for key,value in quantities.items():
          #Converting key string into int 
          key=int(key)
          for product in products:
             if product_ids==key:
                if product.is_sale:
                   total=total+(product.sale_price*value)
                else:
                    total=total+(product.price*value)
                   

       return total

       

    def __len__(self):
      return len(self.cart)
     
    def get_prods(self):  
          #Get ids from cart
         product_ids=self.cart.keys()
          #Use ids to lo lookup products in database model 
         products=Items.objects.filter(id__in=product_ids)

         return products
    
    def get_quants(self):
      quantities=self.cart
      return quantities
    
    def update(self,product,quantity):
       product_id=str(product)
       product_qty=int(quantity)


       {'4':3,"2":5}
       #Get Cart
       outcart=self.cart
       #Update Dictionary/cart
       outcart[product_id,]=product_qty

       self.session.modified=True

        
       if self.request.user.is_authenticated:
        #Get the current user Profile
        current_user=Profile.objects.filter(user__id=self.request.user.id)
        #Convert {'3':1,'2':4} to {"3":1,"2":4 }
        carty=str(self.cart)
        carty=carty.replace("\'","\"")
        #Save the carty to Profile Model
        current_user.update(old_cart=str(carty))

       thing=self.cart
       return thing 
    
    def delete(self,product):
       
       product_id=str(product)
       #Delete from cart
       if product_id in self.cart:
         
          del self.cart[product_id]

       self.session.modified=True 
       if self.request.user.is_authenticated:
        #Get the current user Profile
        current_user=Profile.objects.filter(user__id=self.request.user.id)
        #Convert {'3':1,'2':4} to {"3":1,"2":4 }
        carty=str(self.cart)
        carty=carty.replace("\'","\"")
        #Save the carty to Profile Model
        current_user.update(old_cart=str(carty))
 
          
