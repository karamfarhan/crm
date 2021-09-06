
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import CustomerSerializers, OrderSerializers, ProductSerializers, RegisterSerializers , UserSerializers
from acounts.models import Customer, Product , Order , User




@api_view(['GET'])
def apiview(request):

    api_urls ={
        '/api/acounts/customer/pk/' : 'customer detile',
        '/api/acounts/update_customer/pk/' : 'update customer ',
        '/api/acounts/create_customer/' : 'create customer ',
        '/api/acounts/delete_customer/pk/' : 'delet ecustomer ',



        'api/acounts/product/pk' : 'produduct detile',
        'api/acounts/order/pk' : 'order detile',
        'api/createorder': 'create order',
        'api/updateorder/<str:pk>': 'update order ',
        'api/deleteorder/<str:pk>': 'delete order',
    }


    return Response(api_urls)




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def apicustomer(request,pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if customer.user != user:
        return Response({'Error':'you canot make premation '})

    if request.method == 'GET':
    
        serializers = CustomerSerializers(customer)
        return Response(serializers.data)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def apicustomer_create(request):
    getuser = request.user

    customer = Customer(user=getuser)

    if request.method == 'POST':
        serializers = CustomerSerializers(customer ,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def apicustomer_update(request,pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if customer.user != user:
        return Response({'Error':'you canot make premaion '})


    if request.method == 'PUT':
        data = {}
        serializers = CustomerSerializers(instance=customer,data=request.data)
        if serializers.is_valid():
            serializers.save()
            #data['success'] = "customer was UPdated"
            return Response(serializers.data) # (data=data)
        
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def apicustomer_delete(request,pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if customer.user != user:
        return Response({'Error':'you canot make premaiton'})

    if request.method == 'DELETE':
        opration = customer.delete()
        data = {}
        if opration:
            data['success'] = "customer was deleted"
        else:
            data['feild'] = "delete feild !!!!!!!!"
        return Response(data=data)
         




class apicustomerlist(ListAPIView):
    serializer_class = CustomerSerializers
    pagination_class = PageNumberPagination  # http://127.0.0.1:7000/api/acounts/customers/?page=2
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,OrderingFilter) # http://127.0.0.1:7000/api/acounts/customers/?search=karam
                                                    # http://127.0.0.1:7000/api/acounts/customers/?search=karam&ordering=-date_created

    search_fields = ('name','adress','user__username')


    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user).order_by('-date_created')





class apilogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post (self, request):
        data = {}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user  =authenticate(username=username,password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            data['response'] = 'succcessfully authenticate'
            data['pk'] = user.pk
            data['username'] = username
            data['token'] =  token.key

        else:
            data['response'] = 'Error'
            data['error message'] = 'invalid authenticate'
        return Response(data)



@api_view(['POST'])
def apiregister(request):
    
    if request.method == 'POST':
        serializers = RegisterSerializers(data=request.data)
        data = {}
        if serializers.is_valid():
            user = serializers.save()
            data['Responce'] = 'successfuly registerions new user'
            data['Username'] = user.username
            data['Email'] = user.email
            token = Token.objects.get(user=user).key
            data['Token'] = token
        else:
            data = serializers.errors
        return Response(data)





@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def apiuser_detil(request):
    
    try: 
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = UserSerializers(user)
        return Response(serializers.data)
    




@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def apiuser_update(request):

    try: 
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method  == 'PUT':
        serializers = UserSerializers(instance=user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



























@api_view(['GET'])
def apipruduct(request,pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':

        serializers = ProductSerializers(product)
        return Response(serializers.data)


@api_view(['GET'])
def apiorder(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializers = OrderSerializers(order)
        return Response(serializers.data)







@api_view(['POST'])
def apicreateorder(request):
    serializers = OrderSerializers(data=request.data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)

@api_view(['POST'])
def apiupdateorder(request,pk):
    order = Order.objects.get(id=pk)
    serializers = OrderSerializers(instance=order, data=request.data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)

@api_view(['DELETE'])
def apideleteorder(request,pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return Response("deleted is TRUE")
