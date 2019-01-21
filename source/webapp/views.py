from django.views.generic import DetailView, CreateView, UpdateView, View, ListView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from webapp.models import Food, Order, OrderFood, User
from webapp.forms import FoodForm, OrderForm, OrderFoodForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404

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


class OrderDetailView(FormView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    form_class = OrderFoodForm
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
    permission_required = 'webapp.add_orderfood'

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        form.instance.order = order
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk,
            'edit_url': reverse('webapp:order_food_update', kwargs={'pk': order_food.pk})
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
        }, status='422')


class OrderFoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    permission_required = 'webapp.change_orderfood'

    def form_valid(self, form):
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
}, status='422')

# class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = OrderFood
#     template_name = 'order_food_delete.html'
#     permission_required = 'webapp.delete_orderfood'
#
#     def get_success_url(self):
#         return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    permission_required = 'webapp.delete_orderfood'

    def delete(self, request, *args, **kwargs):
        self.object = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        pk = self.object.pk
        self.object.delete()
        return JsonResponse({
            'pk': pk
        })


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

