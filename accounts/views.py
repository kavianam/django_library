from django.views import generic
from django.urls import reverse_lazy

from .forms import SignUpForm


class Register(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# class Register(View):
#     def get(self, request):
#         return render(request, 'registration/register.html')
#
#     def post(self, request, *args, **kwargs):
#         print(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = get_user_model().objects.create_user(username, password=password)
#         return HttpResponse(f"User {user} registered!")
