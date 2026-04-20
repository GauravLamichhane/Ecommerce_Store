from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.permissions import IsAdminOrReadOnly, ViewCustomerHistory
from .models import (
    Order,
    Product,
    Collection,
    OrderItem,
    ProductImage,
    Review,
    Cart,
    CartItem,
    Customer,
)
from .serializers import (
    CreateOrderSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductImageSerialier,
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
    UpdateOrderSerializer,
)
from .filters import ProductFilter
from .pagination import DefaultPagination

"""Viewsets"""


class ProductViewSet(ModelViewSet):
    # filtering using djangofilter
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    """ Manual Filtering"""
    # def get_queryset(self):
    #   queryset = Product.objects.all()
    #   collection_id = self.request.query_params.get('collection_id')
    #   if collection_id is not None:
    #     queryset = queryset.filter(collection_id = collection_id)

    #   return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product cant be deleted because it is associated with an orderitem."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #   product = get_object_or_404(Product, pk = pk)
    #   if product.orderitems.count() > 0:
    #     return Response({'error':'Product cant be deleted because it is associated with an orderitem.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #   product.delete()
    #   return Response(status=status.HTTP_404_NOT_FOUND)


"""Generic classbased APIVIEW"""
# class ProductList(ListCreateAPIView):
#   queryset = Product.objects.select_related('collection').all()
#   serializer_class = ProductSerializer

#   def get_serializer_context(self):
#     return {'request':self.request}

"""Class Based Views"""
# class ProductList(APIView):
#   def get(self, request):
#     queryset = Product.objects.select_related('collection').all()
#     serializer = ProductSerializer(queryset, many = True, context = {'request':request})
#     return Response(serializer.data)
#   def post(self, request):
#     serializer = ProductSerializer(data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

"""Function Based Views"""
# @api_view(['GET','POST'])
# def product_list(request):
#   if request.method == 'GET':
#     queryset = Product.objects.select_related('collection').all()
#     serializer = ProductSerializer(queryset, many = True, context = {'request':request})
#     return Response(serializer.data)
#   elif request.method == 'POST':
#     serializer = ProductSerializer(data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer

#   def delete(self, request, pk):
#     product = get_object_or_404(Product, pk = pk)
#     if product.orderitems.count() > 0:
#       return Response({'error':'Product cant be deleted because it is associated with an orderitem.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     product.delete()
#     return Response(status=status.HTTP_404_NOT_FOUND)


# class ProductDetail(APIView):
#   def get(self, request, pk):
#     product = get_object_or_404(Product, pk = pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)
#   def put(self, request, pk):
#     product = get_object_or_404(Product, pk = pk)
#     serializer = ProductSerializer(product, data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
#   def delete(self, request, pk):
#     product = get_object_or_404(Product, pk = pk)
#     if product.orderitems.count() > 0:
#       return Response({'error':'Product cant be deleted because it is associated with an orderitem.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     product.delete()
#     return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET','PUT','DELETE'])
# def product_detail(request, pk):
#   product = get_object_or_404(Product, pk = pk)
#   if request.method == 'GET':
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)
#   elif request.method == 'PUT':
#     serializer = ProductSerializer(product, data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
#   elif request.method == 'DELETE':
#     if product.orderitems.count() > 0:
#       return Response({'error':'Product cant be deleted because it is associated with an orderitem.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     product.delete()
#     return Response(status=status.HTTP_404_NOT_FOUND)

"""Collection Viewset"""


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()

        if collection.product_set.exists():
            return Response(
                {
                    "error": "Collection cannot be deleted because it contains one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #   collection = get_object_or_404(Collection, pk = pk)
    #   if collection.products.count() > 0:
    #     return Response({'error':'Collection cannot be deleted because it contains one or more products.'},status = status.HTTP_404_NOT_FOUND)
    #   collection.delete()
    #   return Response(status = status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):
#   queryset = queryset = Collection.objects.annotate(
#       products_count = Count('product')
#     ).all()
#   serializer_class = CollectionSerializer

# @api_view(['GET','POST'])
# def collection_list(request):
#   if request.method == 'GET':
#     queryset = Collection.objects.annotate(
#       products_count = Count('product')
#     ).all()
#     serializer = CollectionSerializer(queryset, many = True)
#     return Response(serializer.data)
#   elif request.method == 'POST':
#     #deserializing the data
#     serializer = CollectionSerializer(data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status= status.HTTP_201_CREATED)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#   queryset = Collection.objects.annotate(
#     products_count = Count('product'))
#   serializer_class = CollectionSerializer

#   def delete(self, request, pk):
#     collection = get_object_or_404(Collection, pk = pk)
#     if collection.product_set.count() > 0:
#       return Response({'error':'Collection cannot be deleted because it contains one or more products.'},status = status.HTTP_404_NOT_FOUND)
#     collection.delete()
#     return Response(status = status.HTTP_204_NO_CONTENT)


# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request, pk):
#   collection = get_object_or_404(Collection.objects.annotate(
#     products_count = Count('product')
#   ), pk = pk)
#   if request.method == 'GET':
#     serializer = CollectionSerializer(collection)
#     return Response(serializer.data)
#   elif request.method == 'PUT':
#     serializer = CollectionSerializer(collection, data = request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
#   elif request.method == 'DELETE':
#     if collection.product.count() > 0:
#       return Response({'error':'Collection cannot be deleted because it contains one or more products.'},status = status.HTTP_404_NOT_FOUND)
#     collection.delete()
#   return Response(status = status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    # url_router extracts product_pk from POST /products/5/reviews/ and stored in self.kwargs => self.kwargs = {
    # 'product_pk': 5 }
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):

    def get_serializer_class(self):
        self.http_method_names = ["get", "post", "patch", "delete"]
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"]).select_related(
            "product"
        )


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, permission_classes=[ViewCustomerHistory])
    def history(self, request, pk):
        return Response("ok")

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        customer = Customer.objects.get(user=request.user)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data)


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only("id").get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerialier

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
