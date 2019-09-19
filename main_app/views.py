
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import DetailView, ListView

from django.http import HttpResponseRedirect
from django.utils.functional import lazy
from django.urls import reverse


import requests 
import uuid
import boto3
from .models import Superhero, Photo, Power


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'superheroes-project'


# Create your views here.


class SuperheroCreate(LoginRequiredMixin, CreateView):
  model = Superhero
  fields = ['name', 'power', 'description', 'age']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class SuperheroUpdate(LoginRequiredMixin, UpdateView):
  model = Superhero
  # Let's disallow the renaming of a Superhero by excluding the name field!
  fields = ['name', 'description', 'age']

class SuperheroDelete(LoginRequiredMixin, DeleteView):
  model = Superhero
  success_url = '/superheroes/'

# Create your views for powers! 
class PowerCreate(LoginRequiredMixin, CreateView):
  model = Power
  fields = '__all__'

class PowerDetail(LoginRequiredMixin, DetailView):
  model = Power

class PowerDelete(LoginRequiredMixin, DeleteView):
  model = Power
  success_url = '/powers/'

class PowerUpdate(LoginRequiredMixin, UpdateView):
  model = Power
  fields = '__all__'

class PowerList(LoginRequiredMixin, ListView):
  model = Power
  
class PhotoDelete(LoginRequiredMixin, DeleteView):
  model = Photo
  def get_success_url(self):
    print("SELF OBJECT", self.object)
    return reverse('detail', kwargs={'superhero_id': self.object.superhero_id})
  # success_url = lazy(reverse,str)('detail', kwargs={})

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
      return redirect('superheroes')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Add new view
@login_required
def superheroes(request):
  response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
  dictionary = response.json()
  superheroes = Superhero.objects.all()
  return render(request, 'superheroes/index.html', { 
    'superheroes': superheroes,
     'dictionary': dictionary
    
    })
@login_required
def superheroes_detail(request, superhero_id):
  superhero = Superhero.objects.get(id=superhero_id)
  power_superhero_doesnt_have = Power.objects.exclude(id__in = superhero.add_powers.all().values_list('id'))
  return render(request, 'superheroes/detail.html', { 
    'superhero': superhero, 
    'add_powers': power_superhero_doesnt_have
  })

# powers view 
@login_required
def powers(request):
  powers = Power.objects.all()
  return render(request, 'main_app/superpower_add.html', { 'powers': powers })
@login_required
def assoc_power(request, superhero_id, power_id):
  Superhero.objects.get(id=superhero_id).add_powers.add(power_id)
  return redirect('detail', superhero_id=superhero_id)

@login_required
def unassoc_power(request, superhero_id, power_id):
  Superhero.objects.get(id=superhero_id).add_powers.remove(power_id)
  return redirect('detail', superhero_id=superhero_id)


@login_required
def add_photo(request, superhero_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to superhero_id or superhero (if you have a superhero object)
            photo = Photo(url=url, superhero_id=superhero_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', superhero_id=superhero_id)




# Define the home view
def home(request):
  return render(request, 'home.html')
def about(request):
  return render(request, 'about.html')


