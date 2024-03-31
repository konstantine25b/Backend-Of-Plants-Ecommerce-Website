from django.core.management.base import BaseCommand
from users.models import CustomUser
from faker import Faker
import random
from products.models import SubCategory ,Product
from orders.models import Order ,OrderItem
from reviews.models import Review

class Command(BaseCommand):
    help = "Populate the database with fake data"
    
    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(45):
            is_staff = random.choice([True] + [False] * 9)  # True once in 10 times
            if is_staff:
                role = 'Admin'
            else:
                role = random.choice(['Customer', 'Vendor'])

            phone_number = fake.phone_number()[:16]  # Truncate phone number if it exceeds 16 characters

            CustomUser.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=phone_number,
                role=role,
                is_superuser=False,
                is_staff=is_staff,
            )
            
            
        
      
        vendors = CustomUser.objects.filter(role='Vendor') 
        subcategories = SubCategory.objects.all()
        
        for _ in range(200):
            vendor = random.choice(vendors)
            subcategory = random.choice(subcategories)

            product = Product(
                vendor=vendor,
                subcategory=subcategory,
                title=fake.word().capitalize(),
                description=fake.text(),
                price=random.uniform(5.0, 100.0),  # Generate random price between 5.0 and 100.0
                quantity=random.randint(0, 100),  # Generate random quantity between 0 and 100
                image_url=fake.image_url(),  # Generate fake image URL
                size=random.choice(['S', 'M', 'L', 'XS' ,'XL', 'XXL']),  # Random size
                is_featured=fake.boolean(),  # Random boolean value
                is_active=True  # Set to active by default
            )
            product.save()
            
        customers = CustomUser.objects.filter(role='Customer') 
        products = Product.objects.all()
        
        for _ in range(105):  # Generate 5 orders
                customer = random.choice(customers)
    
                order = Order.objects.create(
                    customer=customer,
                   
                )
    
                total_items = random.randint(1, 5)  # Generate random number of items for each order
    
                for _ in range(total_items):
                    product = random.choice(products)
                    quantity = random.randint(1, 3)  # Generate random quantity for each product
    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        customer=customer,
                       
                    )
            
                order.save()
                
        for _ in range(130):  # Generate between 0 and 5 reviews
                customer = random.choice(customers)
                rating = random.randint(1, 5)
                comment = fake.text()

                Review.objects.create(
                    product=product,
                    user=customer,
                    rating=rating,
                    comment=comment,
                )
        
        
        