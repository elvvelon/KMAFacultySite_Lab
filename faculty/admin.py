from django.contrib import admin
from .models import Department, Specialty, Lecturer, HomePageContent, ExchangeProgram

admin.site.site_header = "Факультет гуманітарних наук НаУКМА — Панель керування"
admin.site.site_title = "ФГН НаУКМА Адміністрування"
admin.site.index_title = "Управління факультетом та контентом сайту"


class SpecialtyInline(admin.TabularInline):
    model = Specialty
    extra = 1
    fields = ("code", "name", "coordinator_name", "coordinator_contact")
    show_change_link = True


class LecturerInline(admin.TabularInline):
    model = Lecturer
    extra = 1
    fields = ("name", "position", "degree", "email")
    show_change_link = True


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head", "get_specialties_count", "get_lecturers_count", "office")
    search_fields = ("name", "head", "office")
    inlines = [SpecialtyInline, LecturerInline]

    @admin.display(description="К-сть спеціальностей")
    def get_specialties_count(self, obj):
        return obj.specialties.count()

    @admin.display(description="К-сть викладачів")
    def get_lecturers_count(self, obj):
        return obj.lecturers.count()


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "coordinator_name", "coordinator_contact")
    list_filter = ("department",)
    search_fields = ("name", "code", "coordinator_name", "coordinator_contact")
    fieldsets = (
        ("Загальні відомості", {
            "fields": ("code", "name", "department")
        }),
        ("Опис програми", {
            "fields": ("description",),
            "description": "Повний опис спеціальності. На сторінці списку відображатимуться перші 50 слів."
        }),
        ("Координатор набору", {
            "fields": ("coordinator_name", "coordinator_contact"),
        }),
        ("Навчальний план та дисципліни", {
            "fields": ("disciplines",),
            "description": "Введіть список дисциплін (кожна дисципліна з нового рядка або через кому)."
        }),
    )


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "position", "degree", "email")
    list_filter = ("department", "position")
    search_fields = ("name", "department__name", "position", "degree")


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ("title", "dean_name", "phone", "email", "updated_at")
    fieldsets = (
        ("Головний банер та опис", {
            "fields": ("title", "tagline", "description", "history_and_mission")
        }),
        ("Деканат", {
            "fields": ("dean_name", "dean_degree", "dean_message")
        }),
        ("Контактні дані", {
            "fields": ("address", "phone", "email", "working_hours")
        }),
    )

    def has_add_permission(self, request):
        if HomePageContent.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(ExchangeProgram)
class ExchangeProgramAdmin(admin.ModelAdmin):
    list_display = ("university", "languages", "places", "deadline")
    list_filter = ("deadline",)
    search_fields = ("university", "languages", "description")