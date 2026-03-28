from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from recipes.forms import Recipe
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('recipes:index')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)  # ← вот так
        return super().form_valid(form)

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Пагинация для рецептов
        recipes_list = Recipe.objects.filter(author=user).order_by('-date')
        paginator = Paginator(recipes_list, 12)
        page_number = self.request.GET.get('page')
        recipes_page = paginator.get_page(page_number)

        context['recipes'] = recipes_page
        context['recipes_count'] = recipes_list.count()
        context['join_date'] = user.date_joined.strftime('%B %Y')
        context['profile'] = user.profile
        return context


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'users/profile_edit.html', {
            'u_form': u_form,
            'p_form': p_form
        })

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile', username=request.user.username)

        return render(request, 'users/profile_edit.html', {
            'u_form': u_form,
            'p_form': p_form
        })