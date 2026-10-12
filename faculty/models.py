from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва кафедри")
    head = models.CharField(max_length=255, verbose_name="Завідувач кафедри")
    description = models.TextField(blank=True, verbose_name="Опис кафедри")
    email = models.EmailField(blank=True, verbose_name="Електронна пошта")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Контактний телефон")
    office = models.CharField(max_length=100, blank=True, verbose_name="Аудиторія / Корпус")

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедри"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва спеціальності")
    code = models.CharField(max_length=20, verbose_name="Код спеціальності")
    description = models.TextField(verbose_name="Опис")
    coordinator_name = models.CharField(max_length=255, verbose_name="Імʼя координатора набору")
    coordinator_contact = models.CharField(max_length=255, verbose_name="Контакт координатора набору")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="specialties",
        verbose_name="Випускова кафедра"
    )
    disciplines = models.TextField(
        verbose_name="Список дисциплін",
        help_text="Перелік дисциплін (вказуйте кожну дисципліну з нового рядка або через кому)"
    )

    class Meta:
        verbose_name = "Спеціальність"
        verbose_name_plural = "Спеціальності"
        ordering = ["code", "name"]

    def __str__(self):
        return f"{self.code} {self.name}"

    @property
    def short_description(self):
        words = self.description.split()
        if len(words) > 50:
            return " ".join(words[:50]) + "..."
        return self.description

    @property
    def disciplines_list(self):
        if not self.disciplines:
            return []
        lines = [line.strip() for line in self.disciplines.splitlines() if line.strip()]
        if len(lines) == 1 and "," in lines[0]:
            return [item.strip() for item in lines[0].split(",") if item.strip()]
        return lines


class Lecturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Імʼя викладача")
    position = models.CharField(max_length=255, verbose_name="Посада")
    degree = models.CharField(max_length=255, verbose_name="Науковий ступінь")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="lecturers",
        verbose_name="Кафедра"
    )
    email = models.EmailField(blank=True, verbose_name="Електронна пошта")

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.position})"


class HomePageContent(models.Model):
    title = models.CharField(
        max_length=255,
        default="Факультет гуманітарних наук НаУКМА",
        verbose_name="Заголовок головної сторінки"
    )
    tagline = models.CharField(
        max_length=255,
        default="Традиція критичного мислення, інтелектуальної свободи та культурного поступу",
        verbose_name="Слоган факультету"
    )
    description = models.TextField(
        verbose_name="Опис факультету",
        help_text="Основний текст про факультет на головній сторінці"
    )
    history_and_mission = models.TextField(
        blank=True,
        verbose_name="Історія та місія",
        help_text="Розділ про місію, цінності та академічні стандарти"
    )
    dean_name = models.CharField(
        max_length=255,
        default="Ткачук Марина Володимирівна",
        verbose_name="Декан факультету"
    )
    dean_degree = models.CharField(
        max_length=255,
        default="Доктор філософських наук, професор",
        verbose_name="Вчений ступінь та звання декана"
    )
    dean_message = models.TextField(
        blank=True,
        verbose_name="Звернення / вітальне слово декана"
    )
    address = models.CharField(
        max_length=255,
        default="04070, м. Київ, вул. Григорія Сковороди, 2, 1-й корпус НаУКМА, ауд. 201",
        verbose_name="Адреса"
    )
    phone = models.CharField(
        max_length=100,
        default="+38 (044) 425-60-59",
        verbose_name="Контактний телефон"
    )
    email = models.EmailField(
        default="fgn@ukma.edu.ua",
        verbose_name="Електронна пошта"
    )
    working_hours = models.CharField(
        max_length=255,
        default="Понеділок – Пʼятниця: 09:00 – 18:00",
        verbose_name="Графік роботи"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Останнє оновлення")

    class Meta:
        verbose_name = "Текст головної сторінки"
        verbose_name_plural = "Текст головної сторінки"

    def __str__(self):
        return f"{self.title} (Оновлено: {self.updated_at.strftime('%d.%m.%Y %H:%M') if self.updated_at else 'щойно'})"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create(
                title="Факультет гуманітарних наук НаУКМА",
                tagline="Традиція критичного мислення, інтелектуальної свободи та культурного поступу",
                description=(
                    "Факультет гуманітарних наук (ФГН) Національного університету «Києво-Могилянська академія» — "
                    "це інтелектуальне серце Академії, де класичні гуманітарні традиції поєднуються із сучасними "
                    "міждисциплінарними дослідженнями. Факультет забезпечує ґрунтовну освіту в галузях філософії, "
                    "історії, археології, літературознавства, мовознавства та культурології, формуючи вміння глибоко "
                    "аналізувати тексти, смисли, історичні процеси та соціокультурні явища."
                ),
                history_and_mission=(
                    "Місія ФГН — плекати вільну, критично мислячу та відповідальну особистість, здатну осмислювати "
                    "виклики минулого і сьогодення, творити нові культурні наративи та утверджувати субʼєктність України "
                    "у світовому гуманітарному просторі. Наші випускники — це провідні дослідники, викладачі, публічні інтелектуали, "
                    "культурні менеджери, дипломати, перекладачі, видавці та експерти аналітичних центрів."
                ),
                dean_name="Ткачук Марина Володимирівна",
                dean_degree="Доктор філософських наук, професор",
                dean_message=(
                    "Дорогі друзі, колеги та майбутні спудеї! Гуманітарне знання — це фундамент людської гідності, "
                    "самоусвідомлення та спроможності розрізняти сенси серед інформаційного шуму. На Факультеті гуманітарних наук "
                    "ми вчимо не просто запам'ятовувати факти, а ставити сміливі запитання, шукати першоджерела і мислити без догм. "
                    "Запрошуємо вас до нашого академічного кола пошуку й натхнення!"
                ),
                address="04070, м. Київ, вул. Григорія Сковороди, 2, 1-й корпус, ауд. 201",
                phone="+38 (044) 425-60-59",
                email="humanities@ukma.edu.ua",
                working_hours="Понеділок – Пʼятниця: 09:00 – 18:00",
            )
        return obj

class ExchangeProgram(models.Model):
    university = models.CharField(
        max_length=255,
        verbose_name="Університет"
    )
    languages = models.CharField(
        max_length=255,
        verbose_name="Мови навчання"
    )
    places = models.CharField(
        max_length=50,
        verbose_name="Кількість місць"
    )
    deadline = models.DateField(
        verbose_name="Дедлайн подачі"
    )
    description = models.TextField(
        verbose_name="Опис"
    )
    class Meta:
        verbose_name = "Програма обміну"
        verbose_name_plural = "Програми обміну"
        ordering = ["deadline"]
