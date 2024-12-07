from rest_framework import viewsets
from .serializers import ProductSerializer, CustomerSerializer, OrderSerializer
from .models import Product, Customer, Order
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .forms import ProductForm
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly



class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductListView(ListView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'
    success_url = '../../products/'
    def form_valid(self, form):
        return super().form_valid(form)
