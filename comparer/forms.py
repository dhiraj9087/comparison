from django import forms

class SearchForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=100)
