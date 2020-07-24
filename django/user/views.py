from django.shortcuts import render
from django.contrib.auth.forms import (
    UserCreationForm
)
from django.urls import (
    reverse,
    reverse_lazy
)
from django.views.generic import (
    CreateView
)


# revers in used with FBVs
# reverse_laze is used with CBVs
class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    print(UserCreationForm)
    success_url = reverse_lazy('core:MovieList')

    # def get_success_url(self):
    #     return reverse('core:MovieList')

