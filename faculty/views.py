from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Department, Specialty, Lecturer, HomePageContent


def home_view(request):
    """
    Faculty description and key information.
    """
    home_content = HomePageContent.get_solo()
    departments = Department.objects.prefetch_related('specialties', 'lecturers').all()
    specialties = Specialty.objects.select_related('department').all()

    context = {
        'content': home_content,
        'departments': departments,
        'specialties': specialties,
        'departments_count': departments.count(),
        'specialties_count': specialties.count(),
        'lecturers_count': Lecturer.objects.count(),
    }
    return render(request, 'faculty/home.html', context)


def specialty_list_view(request):
    """
    Displays name, code, brief description,
    name and contact information of the admissions coordinator for each.
    """
    query = request.GET.get('q', '').strip()
    dept_id = request.GET.get('dept', '').strip()

    specialties = Specialty.objects.select_related('department').all()

    if query:
        specialties = specialties.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query) |
            Q(coordinator_name__icontains=query)
        )

    if dept_id.isdigit():
        specialties = specialties.filter(department_id=int(dept_id))

    departments = Department.objects.all()

    context = {
        'specialties': specialties,
        'departments': departments,
        'query': query,
        'selected_dept': int(dept_id) if dept_id.isdigit() else None,
    }
    return render(request, 'faculty/specialty_list.html', context)


def specialty_detail_view(request, pk):
    """
    Title, code, full description, admissions coordinator and their contacts,
    degree-granting department, and the list of taught courses.
    """
    specialty = get_object_or_404(Specialty.objects.select_related('department'), pk=pk)
    other_specialties = Specialty.objects.filter(
        department=specialty.department
    ).exclude(pk=specialty.pk)

    context = {
        'specialty': specialty,
        'other_specialties': other_specialties,
    }
    return render(request, 'faculty/specialty_detail.html', context)


def department_list_view(request):
    """
    Displays department name, department head, and the list of
    specialties offered by this department.
    """
    departments = Department.objects.prefetch_related('specialties', 'lecturers').all()
    context = {
        'departments': departments,
    }
    return render(request, 'faculty/department_list.html', context)


def department_detail_view(request, pk):
    """
    Name, department head, description, contacts, list of affiliated specialties,
    and a full list of faculty members.
    """
    department = get_object_or_404(Department.objects.prefetch_related('specialties', 'lecturers'), pk=pk)
    specialties = department.specialties.all()
    lecturers = department.lecturers.all()

    context = {
        'department': department,
        'specialties': specialties,
        'lecturers': lecturers,
    }
    return render(request, 'faculty/department_detail.html', context)


def contacts_view(request):
    """
    Address, phone number, email, working hours, and location of the dean's office and departments.
    """
    home_content = HomePageContent.get_solo()
    departments = Department.objects.all()

    context = {
        'content': home_content,
        'departments': departments,
    }
    return render(request, 'faculty/contacts.html', context)