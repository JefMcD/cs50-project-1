"""
    this module is for defining forms

    Forms is a class defined in the django module forms
    It provides an API with various methods to create input feilds
    and interact with form fields
    https://docs.djangoproject.com/en/4.1/ref/forms/api/#django.forms.Form
    
    instantiating the class with forms.Form as a parameter
    defines a new class which inherits all the methods of 
    the parent forms.Form class
    
    various form field types explained in#
    https://docs.djangoproject.com/en/4.1/ref/forms/fields/#django.forms.CharField

    The heirarchy is as follows
    FormField -> Form Widget -> HTML
    
    Every Form Field has a corrosponding widget which in turn 
    corrosponds to HTML form element 
    
    eg EmailForm -> widget.EmailInput -> <input type='email'>

"""
    
from django import forms 
import datetime

# Simplest Form
class CommentForm(forms.Form):
    comment = forms.CharField(initial='Hello')
# end CommentForm


class FaveBands(forms.Form):
    empty_value='0O0'
    heavy_metal_band   = forms.CharField(label='Heavy_Metal', initial='Grrrr', max_length=20)
    funk_band  = forms.CharField(label='Funk_Band', initial='Give Up The Funk', max_length=20, required=False)
    indie_band = forms.CharField(initial='Shoplifters Unite', max_length=20,help_text='100 characters max.')
    # CharField widget defaults to TextInput ie <input type="text">

    metal_bands = [('0','Select'),('1', 'AC/DC'),('2','Thin Lizzy'),('3', 'Sabbath'),('4', 'Dio')]
    metal_radio =  forms.ChoiceField(widget=forms.RadioSelect, choices = metal_bands)
    metal_select =  forms.ChoiceField(widget=forms.Select, choices = metal_bands)
    
    rock_out = forms.CharField(widget=forms.Textarea, initial="Rockumentary", help_text='Are the voices here with you now?')
    
    email = forms.EmailField(initial='username@mail.com')
    agree = forms.BooleanField()
    date = forms.DateField(initial=datetime.date.today)

# end class

"""
So within these form elements one needs to be able to 
    1. define all the various attributes
    2. assign class(es) to a form element
    3. assign id to a form element
    4. define _data_ tag identifiers 
    
    
    <input> attributes
    type
    id
    name
    value
    readonly
    disabled
    required
    size
    step
    autofocus
    auocomplete
    maxlength
    list -  references a <datalist>

    min/max values
    placeholder
    pattern - for regex comparison validation
    
    exclusive to email and file types
    multiple
    
    exclusive to image type
    height
    width
    
    
    
"""

"""
    This Class provides the structure to define a specific comic
    then it is called with default details of the comic to populate the form
    A user can then alter these as they wish
    
    This Class demonstrates the use of widget.attrs
    This allows the definition of classes and attribute within forms
    
    The majority of the attributes are common to all input types. Where they are
    specific to a particular type the common ones are left out
    
    Class definition of attributes will define the default state 
    for newly created objects. These can be redefined in the views that use them.
    
    Widget Names used by the various input types are here
    https://docs.djangoproject.com/en/4.1/ref/forms/widgets/#django.forms.Select
    
    HTML Attributes defined here
    https://www.w3schools.com/html/html_form_attributes.asp
    https://www.w3schools.com/tags/tag_textarea.asp
    
    django docs on attrs
    https://docs.djangoproject.com/en/4.1/ref/forms/widgets/
    
"""
class Comic(forms.Form):
    max_chars = 500
    coverTitle = forms.CharField(initial='Metal Hurlant',
                                 widget=forms.TextInput(attrs=
                                        {'size': '40'}))
    coverImage = forms.ImageField()
    
    coverArtist = forms.CharField(label='Cover Artist',
                                  initial='Who did this Masterpiece!?',
                                  widget=forms.TextInput(attrs=
                                        {'id': 'cover_art_id',
                                         'class': 'fancy-style',
                                         'value': 'Artist Name', # Initial parameter defines this
                                         'autofocus': False, # False | True | (default False)
                                         'disabled': False, # False | True (default False)
                                         'readonly': False, # False | True (default False) 
                                         'required': False, # False | True (default True)
                                         'size': 50, # width of field in columns (default 20)
                                         'maxlength': 100, # max number of characters (default unlimited)
                                         'placeholder': 'short hint', # appears when field is empty. will be overwritten by value or initial
                                         'list': 'datalist_name', # refers to the name of a datalist element
                                         'autocomplete': 'on' # on | off (default off)
                                         }))
    
    coverTextarea =forms.CharField(label='Description',
                                   initial='Describe your superpowers and special abilities',
                                   widget=forms.Textarea(attrs=
                                        {'id': 'comic-id',
                                         'class': 'comic-blurb',
                                         'autofocus': False, # False | True | (default False)
                                         'disabled': False, # False | True (default False)
                                         'form': 'form_id', # form textarea belongs to
                                         'maxlength': max_chars,
                                         'readonly': False, # False | True (default False) 
                                         'required': False, # False | True (default True)
                                         'wrap': 'soft', # hard|soft
                                         'name': 'superpowers-name',
                                         'rows': '5',
                                         'cols': '50'}))
    
    number_available = forms.IntegerField(label='Copies Available',
                                          initial=50,
                                          widget=forms.NumberInput(attrs=
                                            {'id': 'copies',
                                             'class': 'copies_class',
                                             'name': 'copies_available',
                                              'min': 10,
                                              'max': 1000
                                          }))
    
    issue_dataset =''
    issue_artists =''
    issue_choices =''
    
    issue = ''
    issue_year =['2018','2019','2020','2021','2022','2023']
    year = forms.DateField(widget=forms.SelectDateWidget(years=issue_year))
    
    free_poster = ''
    
    artist_roster = ['Druilet', 'Caza','Moebius','Crumb','Wison','Pekar','Ito','McD']
    contents_list =''
    email = forms.EmailField(label='email',
                             initial='username@mail.com',
                             widget=forms.EmailInput(attrs=
                                {'id': 'email_id',
                                 'class': 'email_class',
                                 'name': 'email_name'
                                
                            }))
    URL = forms.URLField(label='website',
                        initial='website.com',
                        widget=forms.URLInput(attrs=
                        {'id': 'url_id',
                            'class': 'url_class',
                            'name': 'url_name'
                        
                        }))

# end Comic class










"""
    Validation
    
    When a form instance is defined it has an is_valid() method
    
    If the form is valid
    This returns True if all fields contain valid data or False if there are errors
    If the form is valid the forms data get put in the forms cleaned_data attribute
    
    
    If the form is Invalid
    error will be contained in a variable errors ie form_name.errors
    
    The server side validation is performed on the Field only
    The client side validation is performed on the Input and the Field
    
    for example 
    in the population field here the client side validation will look at the 
    widget attribute min:min_pop AND the Field min_value=min_pop
    
    The server will only look at min_value=min_pop 
    so if not defined it will not be verified on the server
    
    therefore it would make sense to have all the things you want validated to 
    be defined in the field parameters an not rely on the widget attrs
    
"""
class Planet(forms.Form):
    max_field_length =25
    min_pop = 100
    max_pop = 200
    name = forms.CharField(label='Planet Name',
                            widget=forms.TextInput(attrs=
                            {'id':'planet-name_id',
                             'class':'planet-name_class',
                             'name':'planet_name_name',
                             'placeholder': 'Enter your planet name',
                             'maxlength':max_field_length}))
    population = forms.IntegerField(label='Population',
                                    min_value=min_pop,
                                    max_value=max_pop,
                                    widget=forms.NumberInput(attrs=
                                    {'id':'id_pop',
                                     'class':'class_pop',
                                     'name':'name_pop',
                                     #'min':min_pop,
                                     #'max':max_pop                   
                                    }))
#end class Planet

class Instrument_Form(forms.Form):
    instrument_name = forms.CharField(label='Instrument',
                                      initial='',
                                      max_length=35,
                                      widget=forms.TextInput(attrs={
                                          'id':'instrument_id',
                                          'class':'instrument_class',
                                          'name':'instrument_name',
                                      }))
    manufacturer = forms.CharField(label='Maker',
                                   max_length=20)
#end instrument_form




class Bones(forms.Form):
    bone_name: forms.CharField(label='Bone Name',
                               initial='',
                               max_length='20',
                               widget=forms.TextInput(attrs={
                                   'placeholder':'Enter Bone Name'
                               }))
#end Bones
    

