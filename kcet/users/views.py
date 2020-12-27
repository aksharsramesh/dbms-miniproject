from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, StudentDetailsForm, PreviousDegreeForm, KCETResultForm, PUResultForm, FormLastActiveForm, DocumentVerifiedForm
from .models import Student, PreviousDegree, KCETResult, PUResult, FormLastActive, DocumentVerified
from django.views.generic import (
    ListView
)
from django.shortcuts import get_object_or_404


# Create your views here.
def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Your account has been created! You can now login')
      return redirect('login')
  else:
      form = UserRegisterForm()
  return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        s_form = StudentDetailsForm(request.POST)
        p_form = PreviousDegreeForm(request.POST)
        kres_form = KCETResultForm(request.POST)
        pu_form = PUResultForm(request.POST)
        act_form = FormLastActiveForm(request.POST or None)
        if s_form.is_valid() and p_form.is_valid() and kres_form.is_valid() and pu_form.is_valid() and act_form.is_valid():
            
            act_form.instance.created_by = request.user
            
            #if act_form.is_valid():
            act_form.save()
            #else:
             #   messages.success(request, f'FormLastActive Error Occured')
              #  return redirect('profile')
            
            pures = pu_form.save(commit=False)
            #pu_form.save()

            student = s_form.save(commit=False)
            student.user = request.user
            student.pu_roll = pures
            #s_form.save()

            prevdeg = p_form.save(commit=False)
            prevdeg.user = request.user
            #p_form.save()

            kcetres = kres_form.save(commit=False)
            kcetres.user = student
            kcetres.name = student.full_name
            #kres_form.save()
           
            pu_form.save()
            s_form.save()
            p_form.save()
            kres_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('kcet-home')
        else:
            messages.success(request, f'Error Occured')
            return redirect('profile')
    else:
        if request.user.is_authenticated:
            if FormLastActive.objects.filter(created_by=request.user).exists():
                messages.success(request, f'Your details has been filled already!')
                student = Student.objects.get(user=request.user)

                context = {
                    'students': Student.objects.filter(user=request.user),
                    'degrees': PreviousDegree.objects.filter(user=request.user),
                    'results': KCETResult.objects.filter(user=student),
                    #'puresults': PUResult.objects.filter(pu_roll=pu_roll),
                }
                return render(request, 'users/details.html', context)
            else:
                s_form = StudentDetailsForm()
                p_form = PreviousDegreeForm()
                kres_form = KCETResultForm()
                pu_form = PUResultForm()
                act_form = FormLastActiveForm(request.POST)

    context = {
        's_form': s_form,
        'p_form': p_form,
        'kres_form': kres_form,
        'pu_form': pu_form,
        'act_form' : act_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def verify(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            d_form = DocumentVerifiedForm(request.POST)
            if d_form.is_valid():
                student = d_form.save(commit=False)
                student.user = request.user
                student.student = Student.objects.get(id=student.unique_id)
                d_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('kcet-home')
            else:
                messages.success(request, f'Error Occured 1')
                return redirect('profile')
        else:
            d_form = DocumentVerifiedForm()
        context = {
            'd_form': d_form
        }    
        return render(request, 'users/verify.html', context)
    else:
        messages.success(request, f'Error Occured 2')
        return redirect('kcet-home')