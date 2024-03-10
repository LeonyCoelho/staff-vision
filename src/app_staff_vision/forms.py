from django import forms
from .models import Establishment , Sector, Sub_Sector, Position, Shift, Status, Global_Settings, Dashboard_Presets, Preset_Header



class UploadFileForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
    )

class ImageUploadForm(forms.Form):
    logo_image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3' })
    )

class ImageUploadForm_Bg(forms.Form):
    background_image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3'})
    )


class EstablishmentForm(forms.ModelForm):
    class Meta:
        model = Establishment
        fields = ['establishment_name']
        widgets = {
            'establishment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['sector_name']
        widgets = {
            'sector_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }

class SubSectorForm(forms.ModelForm):
    class Meta:
        model = Sub_Sector
        fields = ['subSector_name']
        widgets = {
            'subSector_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_name']
        widgets = {
            'position_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift_name']
        widgets = {
            'shift_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status_name']
        widgets = {
            'status_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }


class PresetForm(forms.ModelForm):
    class Meta:
        model = Dashboard_Presets
        fields = ['preset_name']
        widgets = {
            'preset_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nova entrada'}),
        }
    def save(self, commit=True):
        instance = super(PresetForm, self).save(commit)
        Preset_Header.objects.create(preset=instance, header_width=12)
        return instance