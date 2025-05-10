# forex_app/forms.py
from django import forms

class ImportFileForm(forms.Form):
    file = forms.FileField(label='Archivo CSV')

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file:
            raise forms.ValidationError('No se ha subido ningún archivo.')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('El archivo debe ser un CSV.')
        # Validar formato DAT_MT_[SÍMBOLO]_M1_[AÑO].csv (opcional para pruebas)
        if not file.name.startswith('DAT_MT_'):
            self.add_error('file', 'El archivo debe tener el formato DAT_MT_[SÍMBOLO]_M1_[AÑO].csv (por ejemplo, DAT_MT_USDMXN_M1_2010.csv).')
        return file