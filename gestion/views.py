from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CompanieForm, EmployeeForm, UserForm
from .models import Companie, Employee

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_companie(request):
    if not request.user.is_authenticated():
        return render(request, 'gestion/login.html')
    else:
        form = CompanieForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            companie = form.save(commit=False)
            companie.user = request.user
            companie.companie_logo = request.FILES['companie_logo']
            file_type = companie.companie_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'companie': companie,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'gestion/create_companie.html', context)
            companie.save()
            return render(request, 'gestion/detail.html', {'companie': companie})
        context = {
            "form": form,
        }
        return render(request, 'gestion/create_companie.html', context)


def create_employee(request, companie_id):
    form = EmployeeForm(request.POST or None)
    companie = get_object_or_404(Companie, pk=companie_id)
    if form.is_valid():
        employee = form.save(commit=False)
        employee.companie = companie
        employee.save()
        return render(request, 'gestion/detail.html', {'companie': companie})
    context = {
        'companie': companie,
        'form': form,
    }
    return render(request, 'gestion/create_employee.html', context)


def delete_companie(request, companie_id):
    companie = Companie.objects.get(pk=companie_id)
    companie.delete()
    companie = Companie.objects.filter(user=request.user)
    return render(request, 'gestion/index.html', {'companie': companie})


def delete_employee(request, companie_id, employee_id):
    companie = get_object_or_404(Companie, pk=companie_id)
    employee = Employee.objects.get(pk=employee_id)
    employee.delete()
    return render(request, 'gestion/detail.html', {'companie': companie})


def detail(request, companie_id):
    if not request.user.is_authenticated():
        return render(request, 'gestion/login.html')
    else:
        user = request.user
        companie = get_object_or_404(Companie, pk=companie_id)
        return render(request, 'gestion/detail.html', {'companie': companie, 'user': user})


def favorite(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    try:
        if employee.is_favorite:
            employee.is_favorite = False
        else:
            employee.is_favorite = True
        employee.save()
    except (KeyError, Employee.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_companie(request, companie_id):
    companie = get_object_or_404(Companie, pk=companie_id)
    try:
        if companie.is_favorite:
            companie.is_favorite = False
        else:
            companie.is_favorite = True
        companie.save()
    except (KeyError, Companie.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'gestion/login.html')
    else:
        companies = Companie.objects.filter(user=request.user)
        employee_results = Employee.objects.all()
        query = request.GET.get("q")
        if query:
            companies = companies.filter(
                Q(companie_name__icontains=query) |
                Q(address__icontains=query)
            ).distinct()
            employee_results = employee_results.filter(
                Q(employee_name__icontains=query) |
                Q(employee_surname__icontains=query)
            ).distinct()
            return render(request, 'gestion/index.html', {
                'companies': companies,
                'employee': employee_results,
            })
        else:
            return render(request, 'gestion/index.html', {'companies': companies})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'gestion/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                companie = Companie.objects.filter(user=request.user)
                return render(request, 'gestion/index.html', {'companie': companie})
            else:
                return render(request, 'gestion/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'gestion/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gestion/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                companie = Companie.objects.filter(user=request.user)
                return render(request, 'gestion/index.html', {'companie': companie})
    context = {
        "form": form,
    }
    return render(request, 'gestion/register.html', context)


def employees(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'gestion/login.html')
    else:
        try:
            employee_id = []
            for companie in Companie.objects.filter(user=request.user):
                for employee in companie.employee_set.all():
                    employee_id.append(employee.pk)
            users_employee = Employee.objects.filter(pk__in=employee_id)
            if filter_by == 'favorites':
                users_employee = users_employee.filter(is_favorite=True)
        except Companie.DoesNotExist:
            users_employee = []
        return render(request, 'gestion/employees.html', {
            'employee_list': users_employee,
            'filter_by': filter_by,
        })
