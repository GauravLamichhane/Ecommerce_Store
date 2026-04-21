from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Max, Avg, Sum
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from store.models import Product, Order, OrderItem, Customer, Collection
from templated_mail.mail import BaseEmailMessage

# def say_hello(request):
#     # result = Order.objects.aggregate(count = Count('id'))
#     # result = OrderItem.objects.filter(product__id=1).aggregate(quantiy_counts = Sum('quantity'))
#     # result = Order.objects.filter(customer__id = 1).aggregate(product_count = Count('id'))
#     # result = Product.objects.filter(collection__id = 3).aggregate(
#     #   min_price=Min('unit_price')
#     # Products: inventory < 10 and price < 20
#     # result = Product.objects.filter(inventory__lt = 10, unit_price__lt = 20)
#     # result = Product.objects.filter(inventory__lt = 10).filter(unit_price__lt = 20)

#     # Products: inventory < 10 OR price < 20
#     # result = Product.objects.filter(Q(inventory__lt = 20) & ~Q(unit_price__lt = 20))
#     # result = Product.objects.filter(collection__id = F('unit_price'))
#     # result = Product.objects.order_by('unit_price')[0]# returns a queryset
#     # result = Product.objects.latest('unit_price') # return a object
#     # query_set = Product.objects.values_list('id','title','collection__title')

#     # Select products that have been ordered and sort them by title
#     # query_set = Product.objects.filter(id__in = OrderItem.objects.values('product__id').distinct()).order_by('title')
#     # query_set = Product.objects.only('id','title')
#     # query_set = Product.objects.select_related('collection__someotherfiled').all()
#     """
#     select_related (FK and one-one)

#     “Bring everything in one truck.”

#     prefetch_related(ManyToMany)

#     “Bring items in multiple trucks, then sort at home.”
#     """
#     # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
#     # queryset = Product.objects.annotate(is_new = Value(True))
#     # queryset = Product.objects.annotate(new_id = F('id') + 1)
#     # queryset = Customer.objects.annotate(
#     #   full_name = Func(F('first_name'),Value(' '),
#     #                    F('last_name'), function = 'CONCAT')
#     # )
#     # queryset = Customer.objects.annotate(
#     #   orders_count = Count('order')
#     # )
#     # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field= DecimalField())
#     # queryset = Product.objects.annotate(
#     #   discounted_price = discounted_price
#     # )
#     # queryset = Product.objects.aggregate(total=Sum('unit_price'))
#     # queryset = TaggedItem.objects.get_tags_for(Product, 1)
#     # Collection.objects.filter(pk = 11).update(featured_product = None)
#     # database atomicity property
#     with transaction.atomic():
#         order = Order()
#         order.customer_id = 1
#         order.save()

#         item = OrderItem()
#         item.order = order
#         item.product_id = 1
#         item.quantity = 1
#         item.unit_price = 10
#         item.save()

#     return render(request, "hello.html", {"name": "gaurav"})


def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name="emails/hello.html", context={"name": "gaurav"}
        )
        message.send(["gaurav@gg.com"])
    except BadHeaderError:
        pass
    return render(request, "hello.html", {"name": "Gaurav"})
