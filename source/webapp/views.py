from django.views.generic import DetailView, CreateView, UpdateView, View, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, User
from webapp.forms import FoodForm, OrderForm, OrderFoodForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class FoodDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'food_detail.html'
    permission_required = 'webapp.view_food'

class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm
    permission_required = 'webapp.add_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})

class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm
    permission_required = 'webapp.change_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})

class FoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'food_delete.html'
    permission_required = 'webapp.delete_food'

    def get_success_url(self):
        return reverse('webapp:order_list')

class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.operator = self.request.user
        return super().form_valid(form)

class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    permission_required = 'webapp.view_order'

class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

class OrderFoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'
    permission_required = 'webapp.add_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class OrderFoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_update.html'
    permission_required = 'webapp.change_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    template_name = 'order_food_delete.html'
    permission_required = 'webapp.delete_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

class OrderDeliverView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_deliver'

    def get(self, *args, **kwargs):
        self.object = Order.objects.get(pk=self.kwargs.get('pk'))
        if self.object.status == 'preparing':
            self.object.courier = self.request.user
            self.object.status = 'on_way'
        elif self.object.status == 'on_way' and self.object.courier == self.request.user:
            self.object.status = 'delivered'
        self.object.save()
        return redirect('webapp:order_list')


class OrderRejectView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        self.object = Order.objects.get(pk=self.kwargs.get('pk'))
        self.object.status = 'canceled'
        self.object.save()
        return redirect('webapp:order_list')

class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    permission_required = 'webapp.view_order'

class FoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Food
    template_name = 'food_list.html'
    permission_required = 'webapp.view_food'