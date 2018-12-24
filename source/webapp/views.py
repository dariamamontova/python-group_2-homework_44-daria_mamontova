from django.views.generic import DetailView, CreateView, UpdateView, View, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, User
from webapp.forms import FoodForm, OrderForm, OrderFoodForm
from django.shortcuts import redirect



class FoodDetailView(DetailView):
    model = Food
    template_name = 'food_detail.html'

class FoodCreateView(CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})

class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})

class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'food_delete.html'

    def get_success_url(self):
        return reverse('order_list')

class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})

class OrderFoodCreateView(CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class OrderFoodUpdateView(UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_update.html'

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class OrderDeliverView(View):
    def get(self, *args, **kwargs):
        self.object = Order.objects.get(pk=self.kwargs.get('pk'))
        if self.object.status == 'preparing':
            self.object.status = 'on_way'
        elif self.object.status == 'on_way':
            self.object.status = 'delivered'
        self.object.save()
        return redirect('order_list')
#
class OrderRejectView(View):
    def get(self, *args, **kwargs):
        self.object = Order.objects.get(pk=self.kwargs.get('pk'))
        self.object.status = 'canceled'
        self.object.save()
        return redirect('order_list')

class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'

class FoodListView(ListView):
    model = Food
    template_name = 'food_list.html'