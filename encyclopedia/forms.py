
from django import forms

class wiki_search_form(forms.Form):
    search_term = forms.CharField(label='Search',
                                  initial = '',
                                  max_length = 20,
                                  widget = forms.TextInput(attrs={
                                      'name':'q',
                                      'class':'search',
                                      'placeholder':'Lookup Wiki'
                                  }))
#end wiki_search_form

class wiki_page_form(forms.Form):
    page_title = forms.CharField(label='Title',
                                 initial='',
                                 max_length=45,
                                 widget=forms.TextInput(attrs={
                                     'placeholder':'Enter The Name of The Wiki',
                                     'name': 'wiki_form_title',
                                     'class':'wiki_form_title_input'
                                 }))
    page_content=forms.CharField(label='',
                                 initial='',
                                 widget=forms.Textarea(attrs={
                                     'placeholder':'Enter wiki contents using Markdown',
                                     'name': 'page_content_textarea',
                                     'class': 'pagae_content_class',
                                     'cols': '10',
                                     'rows': '10'
                                 }))
#end wiki_page_form

