
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import Superhero


# Create your views here.


class SuperheroCreate(CreateView):
  model = Superhero
  fields = '__all__'

class SuperheroUpdate(UpdateView):
  model = Superhero
  # Let's disallow the renaming of a Superhero by excluding the name field!
  fields = ['name', 'description', 'age']

class SuperheroDelete(DeleteView):
  model = Superhero
  success_url = '/superheroes/'





def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      # redirect should be changed to 'index'
      return redirect('about')
    else:
      error_message = 'Invalid sign up - keep trying'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Add new view
def superheroes(request):
  superheroes = Superhero.objects.all()
  return render(request, 'superheroes/index.html', { 'superheroes': superheroes })

def superheroes_detail(request, superhero_id):
  superhero = Superhero.objects.get(id=superhero_id)
  return render(request, 'superheroes/detail.html', { 'superhero': superhero })



# Define the home view
def home(request):
  return render(request, 'home.html')
def about(request):
  return render(request, 'about.html')


