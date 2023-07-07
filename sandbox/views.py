# heavily commented version for noobs like me

from django.shortcuts import render
from django.http import HttpResponse

import re
# This imports a module for performing regex functions on strings

from django.core.files.base import ContentFile
# Django source code https://docs.djangoproject.com/en/3.2/_modules/django/core/files/base/
"""
    https://docs.djangoproject.com/en/3.2/ref/files/file/#django.core.files.ContentFile
    class ContentFile(content, name=None)
    A File-like object that takes just raw content, rather than an actual file.
    - Whats the difference ????
    The ContentFile class inherits from File, 
    but unlike File it operates on string content (bytes also supported), rather than an actual file.
    
    What is the Parent File Class ???
    https://docs.djangoproject.com/en/3.2/ref/files/file/#django.core.files.File
    class File(file_object, name=None)
    The File class is a thin wrapper around a Python file object with some Django-specific additions. 
    Internally, Django uses this class when it needs to represent a file.
    
    ie  default_storage.save(filename, ContentFile(content))
    Here the callto ContentFile takes a string (content)  and returns an object of type ContentFile containing the string data
    This ContentFile object is then used as a parameter of the type required by default_storage.save()
    
    
"""


from django.core.files.storage import default_storage
# ???
# _, filenames = default_storage.listdir("entries")
# default_storage.listdir('entries')
# takes the pathname of a directory to query 
# returns a tuple.
# The tuple contains two lists
# first list contains directories within the queried directory
# second list contains filenames within the queried directory
"""
    Managing Files
    https://docs.djangoproject.com/en/1.11/topics/files/
    By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings. 
    
    
    MEDIA_ROOT default location = "" (Empty String)
    (not sure if this is current directory or user home directory - I think its current directory)
    can be redefined as
    MEDIA_ROOT = "/var/www/example.com/media/"
    then uploaded files will be saved here.
    https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-MEDIA_ROOT
    
    MEDIA_URL default = "" (Empty String)
    URL that handles the media served from MEDIA_ROOT, used for managing stored files
    https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-MEDIA_URL
    
   
    
    
    https://docs.djangoproject.com/en/1.8/_modules/django/core/files/storage/
    default_storage = DefaultStorage() (at the very bottom of the page)
    
    https://docs.djangoproject.com/en/1.11/ref/files/storage/#the-storage-class
    
    Why is this function assigned to a variable name ???
    Why doesnt it work if you use DefaultStorage instead of default_storage ???
    changing default_storage to DefaultStorage produces err
    error: type object 'DefaultStorage' has no attribute 'listdir'
    I think this is due to DefaultStorage using a LazyFunction that initialises 
    some magical stuff it needs after its called, so it cant be used directly 
    (unless you know all about how all that works)
    
    In truth I dont know. but to access the file storage functions you need
    to use default_storage which has methods that return file system information 
    and allows you to perform operations such as open close delete
    
    Setting up File Handling is generally done by doing this;
"""
    
    # from django.core.files.storage import default_storage

"""
    Then you have access to the Storage API and all the functions and classes therein
        
"""


# exempler 
def list_edit(request):
    directories, filenames = default_storage.listdir("entries")
    new_filenames = list(sorted(re.sub(r"\.md$", "", filename) 
                                for filename in filenames if filename.endswith(".md")))  
    
    return render(request, 'sandbox/index.html', {
                    "filenames": new_filenames,
                    "wiki_dirs": wiki_dirs,
                    "wiki_files": wiki_files,
                    "liked_fruits": liked_fruits,
                    "disliked_fruits": disliked_fruits 
    })  
# end list_edit






"""
    This next function **list_edit_long** Does the same as the exampler
    but is more easy to understand for noobs 
    
        return list(sorted( re.sub(r"\.md$", "", filename)
                            for filename in filenames if filename.endswith(".md")))
                        
    this looks complex 
    it works like this
    the list() part casts the object to type list()
    
    Inside it is a sorted() function which works like this
    sorted(iterable, key=key, reverse=reverse
    where iterable is The sequence to sort, list, dictionary, tuple etc
    where key is A Function to execute to decide the order. Default is None
    where reverse A Boolean. False will sort ascending, True will sort descending. Default is False
    
    so here the sorted function contains a single expression of two parts (not two parameters)
    the iterable is - (re.sub(r"\.md$","", filename)) 
        ie the list of filenames without the '.md' extension
        
    then the value yielded by a generation expression - (for filename in filenames if filename.endswith(".md")) 

        ( This second part is distinct from a second parameter which 
          would be a key in the case of the sorted method. Thats not whats going on here)
        
        What I want it to do is:
        1. I have a directory containing files and directories
        2. ignore files that do not contain '.md' at the end
        3. ignore directories
        4. sort the remaining files alphabetically
        
        So what is this function in the position of the key parameter doing there?

        There are several python concepts going on here
        1. for in if statement
        
        
        2. list comprehension
        https://www.w3schools.com/python/python_lists_comprehension.asp
        
        The for in if statement is part of a list comprehension statement which has the form
        newlist = [expression for item in iterable if condition == True]
        
        Example
        Only accept items that are not "apple":

        newlist = [x for x in fruits if x != "apple"]
        
        The condition if x != "apple"  will return True for all elements other than "apple", 
        making the new list contain all fruits except "apple".

        The condition is optional and can be omitted:
        
        
        3. generator expression
        https://www.geeksforgeeks.org/generator-expressions/
        The third stage takes the list comprehension and uses it as a generator expression
        The generator expression iterates through the list and on each iteration yields the result as an input to the first expression
        in the enclosing function. ie the re.sub(r"\.md$", "", filename) regex function
        
        so the sequence is
        
        1. perform the generator expression and yeild the next filename
        2. regex function obtains the filename and replaces the '.md' part with ''
        3. goto 1 and yeild next filename until iteration is finished
        4. sort the resulting list
        5. cast the result into type list
        
        Soooo...
        In the general case
        list = [x for x in filenames if x.endswith(".md")]
        
        In the exampler the first x is replaced with the regex expression which uses the yeilded x value as a parameter
        list = [re.sub(r"\.md$", "", x) for x in filenames if x.endswith(".md")]
        
        This first part of the expression then forms the items in the list
        
        
        phew!
        
        
        
    
"""

##################################################################################
#
#   File Ops 
#
#   1. Check if a file exists
#
##################################################################################

from django.core.files import File
from django.core.files.base import ContentFile
import os
# The os.path module allows operating filesystem access
# The os.path module gives information about path environment variables

def file_ops(request):
    
    """
        Python ways
        test_file = 'newfile.txt'
        fileops_directory = 'file_ops'
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, fileops_directory)
    """

  
    
    loc = default_storage.location
    base = default_storage.base_url
    file_permissions = default_storage.file_permissions_mode
    dir_permissions = default_storage.directory_permissions_mode
    


    dir_listing, file_listing = default_storage.listdir('.')
    if default_storage.exists('manage.py'):
        filecheck = 'Success'
    else:
        filecheck = 'Fail'
        
    available_name = default_storage.get_available_name('newfile.py')
    valid_name = default_storage.get_valid_name('new-valid-file.py')
    generated_name = default_storage.generate_filename('new-generated-file.py')
    
    fs_path = default_storage.path('target_file.py')
    
    os_name = os.name
    os_environ = os.environ
    os_environ_home = os_environ['HOME']
    os_curr_dir_list = os.listdir
    #os.chdir('sandbox')
    #os_sandbox_dir = os.listdir
    # default open mode is 'rb' read/binary
    # for read/write open with 'r' or 'w' presumeablt 'w' also allows 'r' access but idk
    # for full list of modes see python docs https://docs.python.org/3/library/functions.html#open
    
    #establish current directory
    current_dir = os.path.dirname('.')
    fileops_dir = 'sandbox/testfiles/'
    files_path = os.path.join(current_dir, fileops_dir)
    new_ls = os.listdir(files_path)
    demofile = 'demofile.txt'
    target_read_file = fileops_dir + demofile
    if(os.path.exists(target_read_file)):
        f = open(target_read_file, 'rt')
        file_contents = f.read
    else:
        file_contents = "file does not exist"
        
    
    # Open a file that doesnt exist in 'wt' write/text mode
    demofile = 'nonexistent.txt'
    target_file = fileops_dir + demofile
    if(not os.path.exists(target_file)):
        f = open(target_file, 'wt')
        file_contents = f.write('randon funny text')
    else:
        f = open(target_file, 'rt')
        file_contents = f.read
    f.close


    demofile1 = default_storage.open('sandbox/testfiles/demofile.txt', 'r')
    demofile2 = default_storage.open('sandbox/testfiles/newdemofile.txt', 'w')
    # demofile3 = default_storage.open('sandbox/testfiles/invalid_demofile.txt', 'r') #Crash File Not Found
    #demofile_contents = ContentFile()
    f1 = ContentFile("esta frase está en español")
    f2 = ContentFile(b"these are bytes")
    
    # 1. Check If a File Exists
    
    
    
    return render(request, 'sandbox/file_ops.html',{
                    'message': 'ENVIRONMENT',
                    'current_dir': 'wiki',
                    'file_path': 'sandbox',
                    'location': loc,
                    'base_url': base,
                    'file_permissions_mode': file_permissions,
                    'dir_permissions_mode': dir_permissions,
                    'dir_listing': dir_listing,
                    'file_listing': file_listing,
                    'filecheck': filecheck,
                    'newfilename': available_name,
                    'validfilename': valid_name,
                    'generatedfilename': generated_name,
                    'fs_path': fs_path,
                    'os_name':os_name,
                    'os_environ':os_environ,
                    'os_environ_home':os_environ_home,
                    'os_curr_dir_list': os_curr_dir_list,
                    'files_path': files_path,
                    'new_ls': new_ls,
                    'read_file_contents': file_contents,
    
    })
#end file_ops






def list_operations(request):
    #Lists are mofifiable and allow the full range of edits
    """
        Create, Insert, Update, Delete, Append, Sorting
    """
    
    # list created using square brackets like an array
    # list can contain any type. here is a list containing strings, integers and tuples
    new_list = [] #null list
    band = ["bob",29,("box1, True"), "frank", 40, ("box9", False), "sheila", 32, ("box12", False)]
    
    # Any sequence can be caste to a list using the list() contructor
    # This will return a list containing all the individual items from the sequence
    
    

    # newList1 = ["ANY ITERABLE SEQUENCE. dict, tuple, set. array"]
    musicians ={"name": "bob", 
                "age": 29, 
                "rating": 10,
                }
    
    muse_tup = ("bob", 29, 10, 29, True)
    muse_set = set(muse_tup)
    muse_range = range(0,11)
    
    muso_dict_list = list(musicians)
    muso_tuple_list = list(muse_tup)
    muso_set_list = list(muse_set)
    muso_range_list = list(muse_range)
    
    
    """
        indexing list items
        first_item[0]
        last_item[-1]
        
        nth_item[n]
        second_last[-2]
        etc
        
        Insert, Update Delete list items
        
        append eg new_list.append["newVal"]
        extend - adds a list to an existing list eg list1.extend(list2)
                or
                list3 = list1 + list2
                
        pop eg  new_list.pop(1)             - removes new_list[1] and returns it as a value
        remove  new_list.remove("greta")    - remove first item with value=greta NOT the index
        clear   new_list.clear()            - removes all items and return a null list
                
        del eg  del(newlist[1])             - deletes new_list[1] simple delete nothing returns
        
        list functions
        for a full list of methds for list, run python then declare eg new_list = []
        >>> new_list. ->TAB ->TAB
        
        useful methods for use on lists
        len(new_list)
        new_list.count
        sorted(new_list, key=func(), reverse=False) - sorts are a whole ballgame of their own
    
    """
    return render(request, 'sandbox/list_operations.html', {
                    "musicians": musicians,
                    "band": band,
                    "muso_dict_list": muso_dict_list,
                    "muso_tuple_list": muso_tuple_list,
                    "muso_set_list": muso_set_list,
                    "muso_range_list": muso_range_list
    })
    
# end list_operations
    
    




def tuple_edits(request):
    # Tuples
    """
        Tuples are analogous to tuples in Relational Databases
        and have much in common with Lists ..
        Can Hold Multiple Values in a Single Variable
        The Order they are defined is preserved
        Duplicate values are possible
        Indexed so attributes can be accessed through index numbers like tup[2] etc
        Arbitrary length
        
        Different from lists
        A tuple is immutable; so it cannot be changed once it is defined
        Values are immutable and ordered so can be hashed and act as a key in a dictionary
        
    """
    
    play_tuple = ("flute", "drums", "saxophone", "banjo", "bass", "piano", "vocals", "fiddle")
    # first how to convert a tuple to a list and carry out operation
    # then perform operations and the convert back to tuple and return
    play_list = list(play_tuple)
    list_to_tuple = tuple(play_list)
    
    # next working directly on the tuple then return the tuple
    # Create Update Delete Insert Append
    
    # Create Tuple
    bob_plays = ("bass","guitar","banjo", "fiddle") #brackets optional
    sheila_plays = tuple(["flute","vocals"])

    # Update, Insert, Delete items in a  Tuple
    # Tuples are immutable and cannot alter their values once defined

    # sheila_plays.append("saxophone")          Nope
    # sheila_plays.insert(1,"recorder")         Nope
    # sheila_plays.delete("recorder")           Nope
    # sheila_plays.update("flute", "whistle")   Nope

    strings_list =  ["bass", "guitar", "harp", "fiddle"]
    wind_list = ["flute", "whistle", "vocals"]
    
    band_instruments = (*strings_list, *wind_list)
    """
        the *wind_list expression unpacks the list and its athough you typed themn in individual- works for all sequence type
        this creates a tuple containing all the items in the strings_list plus all the items in the wind_list
    """

    #Multiple Assignments
    bob_plays, trevor_plays, frank_plays, gabby_plays = strings_list
    
    " Or a database might have a tuple like ..."
    instrument = "bass", "fender", 5, 1500
    name, brand, strings, price = instrument
    """
        for example
        def get_instrument_data(instrument_id):
            # query database data 
            return name, brand, notes, price
        
        instrument, brand, notes, price = guery_instrument_data(5StringBass)
    
        so you could iterate through a set of tuples from a table ssigning them to variables
        and then performing some action
        
        This kind of multiple assignment works for all iterable types
    """
    
    old_band = "bass", "vocals"
    new_band = (*old_band, "guitar")
    # Items are added or removed from a tuple by creating a new one
    
    #the len() function works as expected
    print(f"The band has {len(new_band)} members")
    
    """
        The main takeaway from tuples is that they are immutable and ordered
        They are esentially write protected 
        tuples are a direct analogy to tuples in databases and provide a way
        of handling database queries in a format native to relational databases
    """
    
    
    return render(request, "sandbox/tuples.html", {
                    "play_tuple": play_tuple,
                    "name": name,
                    "brand": brand,
                    "strings": strings,
                    "price": price,
                    "new_band": new_band
                    
        
    })
# end tuple_edits
    



def set_edits():
    pass

def dict_edits():
    pass








def list_edit_long (request):
    # list comprehension examples
    fruits = ["apple", "banana", "orange", "strawberry", "grape", "kiwi", "clementine"]
    liked_fruits =    list(x for x in fruits if x != "kiwi")
    disliked_fruits = list(x for x in fruits if x == "kiwi")


    wiki = default_storage.listdir("entries") # returns a tuple of two lists
    wiki_dirs = wiki[0]
    wiki_files = wiki[1]
    
    filenames = ["file1.md", "file2.md", "file3.md", "file4.md"]
    filenames_list = ["li1.md", "li2.md", "li3.md", "li4.md"]
    filenames_tuple = ("tup1.md", "tup2.md", "tup3.md", "tup4.md")
    filenames_set = {"set1.md", "set2.md", "set3.md", "set4.md"}
    filenames_dict = {}

    i=0
    for filename in filenames:
        if filename.endswith(".md"):
            filenames[i] = re.sub(r"\.md$", "", filename)
            i = i+1
        # endif
    #endfor
    
    return render(request, 'sandbox/index.html', {
                    "filenames": filenames,
                    "wiki_dirs": wiki_dirs,
                    "wiki_files": wiki_files,
                    "liked_fruits": liked_fruits,
                    "disliked_fruits": disliked_fruits 
    })
# end of list_edit_long



def render_form(request):
    
    trigger = "form triggered"
    return render(request, 'sandbox/forms.html', {
                    "form_trigger": trigger 
    })
# end render_form

def basic_form(request):
    message = "Enter Name"
    
    return render(request, "sandbox/basic_form.html", {
                    'confirmation_message': message,
                    'default_value': 'Your Name'
    } )
# end basic_form


    
def basic_form_action(request):
    """
    Form data is passed through the system via the request object so it must
    be extracted from the request using the request.POST method or the request.GET
    method depending on how the request received it.
    
    When the form is submitted, the POST request which is sent 
    to the server will contain the form data
    
    request.POST returns a dictionaty object which can be accessed
    
    request.POST returns QueryDict: {'name': 'value', 'name2': 'value2', etc}
    name_value = request.POST['name']
    """
    message = "form submitted"
    
    method = request.method
    if method == 'POST':
        post = request.POST
        name = "name_in"
        name_value = post[name]
    else:
        post = 'request.GET'
        name = "GET Method Used"
        name_value = "Use POST method for forms that change data on the server"

    return render(request, 'sandbox/basic_form_action.html',{
                    'confirmation_message': message,
                    'POST': post,
                    'method': method,
                    'name': name,
                    'value': name_value
    })
# end basic_form_action



def fave_bands_form(request):
    """
        module forms.py is user defined and contains form definitions
    """
    from .forms import FaveBands, Singer
    
    if request.method == "POST":
        bands_form =  FaveBands(request.POST)
        heavy_metal = request.POST['heavy_metal_band']
        funk = request.POST['funk_band']
        indie = request.POST['indie_band']
        return render(request, 'sandbox/fave_bands_verified.html', {
                        'title_block': 'Fave Bands',
                        'confirmation_message': 'POST: What Are Your Fave Bands',
                        'bands_form': bands_form,
                        'heavy_metal': heavy_metal,
                        'funk': funk,
                        'indie': indie
        })
    else:
        bands_form =  FaveBands()
  
        return render(request, 'sandbox/fave_bands_form.html', {
                        'title': 'Fave Bands',
                        'confirmation_message': 'GET: What Are Your Fave Bands',
                        'bands_form': bands_form,
                      
        })
    
# end django_form_class






"""
    Understanding basic form field types
"""
def fave_bands_form_action(request):
        heavy_metal = request.POST['heavy_metal_band']
        funk = request.POST['funk_band']
        indie = request.POST['indie_band']
        return render(request, 'sandbox/fave_bands_verified.html', {
                        'title': 'Fave Bands: Results',
                        'confirmation_message': 'Fave Bands Results',
                        'bands_form': request.POST,
                        'heavy_metal': heavy_metal,
                        'funk': funk,
                        'indie': indie
        })
# end fave_bands_form_action









"""
    Understanding Form Field Widgets and attributes
    https://docs.djangoproject.com/en/4.1/ref/forms/fields/#django.forms.CharField
    https://docs.djangoproject.com/en/4.1/ref/forms/widgets/#django.forms.Select
    
"""
def comix_form(request):
    from django import forms
    from .forms import Comic
    my_comic = Comic()
    
    class customised_comic_form(Comic):
        coverTitle = forms.CharField(initial='Metal Hurlant',
                                 widget=forms.TextInput(attrs=
                                        {'size': '80'}))
        coverTextarea =forms.CharField(label='Description',
                                   initial='Describe your superpowers and special abilities',
                                   widget=forms.Textarea(attrs=
                                        {'id': 'comic-id',
                                         'class': 'comic-blurb2',
                                         'disabled': True, # False | True (default False)
                                         'rows': '20',
                                         'cols': '30'}))
    #end new_comic_form
    #customising  default Comic Class attributes

    return render(request, 'sandbox/comix_form.html', {
                    'comic_form_title': 'Comic Details',
                    'comic_form': customised_comic_form,
                    
    })
    
#end comix_form












def planets_form(request):
    """
        This form view is to play around with field validation
        https://docs.djangoproject.com/en/4.1/topics/forms/
        https://docs.djangoproject.com/en/4.1/ref/forms/validation/
    """
    from django import forms
    from .forms import Planet   

    if request.method == 'POST':
        home_planet = Planet(request.POST)
        if home_planet.is_valid():
            valid_data = home_planet.cleaned_data
            return render(request, 'sandbox/planet_valid.html', {
                            'welcome': 'Welcome Home Traveller',
                            'valid_data': valid_data
        })
        else:
            home_planet = Planet(request.POST)
            invalid_data = home_planet.errors
            return render(request, 'sandbox/planets_form.html',{
                            'planet_header': "Planet Details have Errors",
                            'errors': invalid_data,
                            'planet_form': home_planet
        })
    else:
        home_planet = Planet()
        return render(request, 'sandbox/planets_form.html',{
                        'planet_header': "Planet Details",
                         'planet_form': home_planet
        })
#end planets_form








"""
When to use render template and when to use redirect

Redirect is generally for when you are finished processing the POST data
For example. You gather form data, dropit in an email and send it
POST data processing is finished so you redirect to a confirmation page

from stack overflow
https://stackoverflow.com/questions/21668481/difference-between-render-template-and-redirect

 always do the following:

"GET" method use render_template ("index.html")
"POST" method use redirect("/")
Even though (in this example) both will show the same web page, the dynamic data within may be different due to 
different methods. As we know, GET is as simple as a click in a hyperlink on web page while POST is submitting web 
form which may involve calculation of data and may show in the final web page.

Another supporting recommendation from "Flask Web Development" book by Miguel Grinberg (O'Reilly, 2018): 
If you submit a form (via POST method), if user refresh the page, an obscure warning will pop-up to ask 
confirmation before submitting the form again. This happens because browser repeat the last request, and 
in this case POST. So it is a good practice to never leave a POST request as the last request sent by browser. 
A 'redirect' issues a GET request for the redirect URL, and that is the page that it displays. Now the last 
request is a GET, so the refresh click works as expected, this good practice is known as POST/Redirect/GET p
attern. So always use ‘redirect’ for POST method.
"""
def instruments_form(request):
    from django import forms
    from django.http import HttpResponseRedirect
    from .forms import Instrument_Form
    
    if request.method == 'POST':
        # validate then redirect
        tele = Instrument_Form(request.POST)
        if tele.is_valid():
            #redirect success
            return HttpResponseRedirect('/instrument_success/')
        else:
            #return form Post data back to instrument_form
            return render(request,'sandbox/instruments_form.html',{
                            'instrument_form': tele
            })
    else:
        # render new form
        tele = Instrument_Form()
        return render(request, 'sandbox/instruments_form.html', {
                        'instrument': tele
        })
        
    
# end instrument_form






"""
    URL's
    
    paths and URL's are a big part of DJango so here is a view is to play with some examples
"""
def bones_urls(request):
    return render(request, 'sandbox/bones_urls.html')
#end dem_bones

def bones_users(request, username, user_id):
    return render(request, 'sandbox/bones_users.html', {
                    'username':username,
                    'user_id': user_id
                    })
#end bones_users



def test_form(request):
    """
        Basic Form to get started
        
        auto_id  -  produces an id as an HTML attribute 
                    derived from the variable name
        
        The form data can be initialised by supplying a dict
        containing key:value pairs corrosponding to the fields
        This will be picked up by the initial paramater of the field
    """
    from .forms import CommentForm
    
    form_data = {'comment':'Enter Comment'}
    comment = CommentForm(form_data)

    print(comment)
    return render(request, 'sandbox/test_form.html',{
                    'comment_form': comment
    })
# test_form
    



#######################################################################
#
#   regex
#
#######################################################################
def regex(request):
    question_str = 'How many chucks does a woodchuck chuck if a woodchuck could chuck wood?'
    
    pattern = re.compile('how', re.IGNORECASE)
    start_match = pattern.match(question_str) #This returns an object - how to get to the contents? 
    chuck_match = re.match(r'chuck',question_str) #match checks only the start of the string so returns None here
    
    pattern = re.compile('chuck', re.IGNORECASE)
    pattern_search = pattern.search(question_str) #finds first occurrence
    
    pattern = re.compile('chuck', re.IGNORECASE)
    pattern_findall = pattern.findall(question_str) # returns a list of all occurrences
    
    header_tag_md = '#Page One'
    pattern = re.compile('#')
    start_match = pattern.match(header_tag_md)
    pattern.sub('<h1>',header_tag_md)
    header_tag_html = pattern.sub('<h1>',header_tag_md) + '</h1>'
    
    header_tag2_md = '##Page One the header tag'
    header_tag_regex = re.compile('##')
    start_match = pattern.match(header_tag2_md)

    header_tag_html = header_tag_regex.sub('<h2>',header_tag2_md) + '</h2>'
    
    bold_tag_md = '**Bold** text here'
    bold_tag_regex = re.compile('[abc]')
    
    tag = bold_tag_regex.search(bold_tag_md)
    
    tag = re.search('[ex]', bold_tag_md)

    bold_tag_html = bold_tag_regex.sub('<b>',bold_tag_md)
       
    
    
    return render(request,'sandbox/regex.html',{
                    'title':'Python Regular Expressions : import re',
                    'start_match': start_match,
                    'chuck_match': chuck_match,
                    'pattern_search': pattern_search,
                    'pattern_findall': pattern_findall,
                    'header_tag_html': header_tag_html,
                    'bold_tag_html': bold_tag_html,
                    'tag': tag,
    })
#end regex






#######################################################################
########################## URL Paths Redirects ########################
#######################################################################

from django.http import HttpResponseRedirect
from django.urls import reverse

def hit_target(request, target='none'):
    return render(request, 'sandbox/target.html',{
                    'target': target
    })
#end hit_target

def process_target(request,target='none'):
    message = 'Ork Addition blood and gore -> '+target
    return HttpResponseRedirect(reverse('hit_moving_target', args=(message,)))
#end process_target







































def rando_func(*args, **kwargs):
    """
        *args is s list of values [5,3,7,'hi', 'pepe']
        **kwargs is a dictionar of key=value pairs {'a=1', 'b=5', "c='pepe'"}
    """
    pass
# end rando_func









def solve_for_x(request):
    nodes = ["network", "you.x", "chair", "are.x", "a.x", "laundry",  "pawn","bicycle", "goon", 
             "smooth", "piano", "snoth", "fedora", "maroon"]
    keydict = {1: "you", 2: "are", 3:"a", 4:"fedora"}
    keydict2 = {"you":1, "are": 2, "a": 3, "snoth": 4}
    keylist = ["you", "are", "a", "piano"]
    keytuple = ("you", "are", "a", "chair")
    keyword_tuples = [
        ('you', 0),
        ('are', 1),
        ('a', 2),
        ('star', 3)
    ]
    sorted_list2 = sorted(keyword_tuples, key=lambda word: word[1])   
    
        
    
        
    sorted_list1 = list(sorted(re.sub(r"\.x$", "", node) for node in nodes if node.endswith('.x')))
    
    from operator import itemgetter, attrgetter
    
    sorted_list3 = sorted(sorted_list1, key=itemgetter(0))   

    return render(request, 'sandbox/solve_for_x.html', {
                            "solve_for_x": sorted_list1,
                            "solve_for_x2": sorted_list2,
                            "solve_for_x3": sorted_list3
    })
    




















