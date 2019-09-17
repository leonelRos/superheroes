
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import DetailView, ListView


import uuid
import boto3
from .models import Superhero, Photo, Power


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'superheroes-project'


# Create your views here.




class SuperheroCreate(CreateView):
  model = Superhero
  fields = ['name', 'power', 'description', 'age']

class SuperheroUpdate(UpdateView):
  model = Superhero
  # Let's disallow the renaming of a Superhero by excluding the name field!
  fields = ['name', 'description', 'age']

class SuperheroDelete(DeleteView):
  model = Superhero
  success_url = '/superheroes/'

# Create your views for powers! 
class PowerCreate(CreateView):
  model = Power
  fields = '__all__'

class PowerDetail(DetailView):
  model = Power

class PowerDelete(DeleteView):
  model = Power
  success_url = '/powers/'

class PowerUpdate(UpdateView):
  model = Power
  fields = '__all__'

class PowerList(ListView):
  model = Power
  
class PhotoDelete(DeleteView):
  model = Photo
  success_url = f'/superheroes/'

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
      error_message = 'Invalid sign up - try again'
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
  power_superhero_doesnt_have = Power.objects.exclude(id__in = superhero.add_powers.all().values_list('id'))
  return render(request, 'superheroes/detail.html', { 
    'superhero': superhero, 
    'add_powers': power_superhero_doesnt_have
  })

# powers view 
def powers(request):
  powers = Power.objects.all()
  return render(request, 'main_app/superpower_add.html', { 'powers': powers })

def assoc_power(request, superhero_id, power_id):
  # Note that you can pass a toy's id instead of the whole object
  Superhero.objects.get(id=superhero_id).add_powers.add(power_id)
  return redirect('detail', superhero_id=superhero_id)



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
            # we can assign to cat_id or cat (if you have a cat object)
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


