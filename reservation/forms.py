from django.forms import ModelForm
from reservation.models import Reservation, CourtSchedule, Court
from django import forms
from django.core.exceptions import ValidationError

DAY_CHOICES = [
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miércoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
    (5, 'Sábado'),
    (6, 'Domingo'),
]

class BookForm(ModelForm):
    date = forms.DateField(
        required=True,
        label="Fecha de reserva",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    day_of_week = forms.ChoiceField(
        choices=DAY_CHOICES, 
        required=True, 
        label="Día de la semana",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    schedule_time = forms.ChoiceField(
        label="Horario disponible",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ["date", "day_of_week", "schedule_time"]
        
    def __init__(self, *args, **kwargs):
        court = kwargs.pop('court', None)
        super().__init__(*args, **kwargs)
        self.fields['schedule_time'].choices = []

        if court:
            data = self.data or self.initial
            selected_day = data.get('day_of_week')

            if selected_day is None:
                first_schedule = CourtSchedule.objects.filter(court=court).order_by('day_of_week').first()
                if first_schedule:
                    selected_day = first_schedule.day_of_week
            
            if selected_day is not None:
                schedules = CourtSchedule.objects.filter(court=court, day_of_week=int(selected_day)).order_by('start_time')
                choices = [(s.pk, f"{s.start_time:%H:%M} - {s.end_time:%H:%M}") for s in schedules]
                self.fields['schedule_time'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        schedule_pk = cleaned_data.get('schedule_time')

        if date and schedule_pk:
            try:
                schedule = CourtSchedule.objects.get(pk=schedule_pk)
            except CourtSchedule.DoesNotExist:
                raise ValidationError("Horario no válido.")

            if date.weekday() != schedule.day_of_week:
                raise ValidationError(
                    "La fecha seleccionada no coincide con el día de la semana del horario."
                )
            
            cleaned_data['schedule_instance'] = schedule

        return cleaned_data
    

class CourtCreateForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la pista',
            'required': True
        })
    )

    type = forms.ChoiceField(
        label="Tipo de pista",
        choices=Court.TYPE_CHOICES,  
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )

    location = forms.CharField(
        label="Ubicación",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ubicación (ej. Polideportivo Central)',
            'required': True
        })
    )

    price = forms.DecimalField(
        label="Precio (€)",
        min_value=0,
        decimal_places=2,
        max_digits=8,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio por hora (€)',
            'step': '0.01',
            'required': True
        })
    )

    class Meta:
        model = Court
        fields = ['name', 'type', 'location', 'price']


class ScheduleCreateForm(forms.ModelForm):
    court = forms.ModelChoiceField(
        queryset=Court.objects.all(),
        label="Pista",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    day_of_week = forms.ChoiceField(
        choices=DAY_CHOICES,
        label="Día de la semana",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_time = forms.TimeField(
        label="Hora de inicio",
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    end_time = forms.TimeField(
        label="Hora de fin",
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )

    class Meta: 
        model = CourtSchedule
        fields = ['court', 'day_of_week', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'court' in kwargs['initial']:
            self.fields['court'].initial = kwargs['initial']['court']
    

