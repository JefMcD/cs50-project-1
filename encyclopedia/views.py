import http
import os
import os.path
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import wiki_search_form, wiki_page_form
from . import util
from . import jefmcd2html



def index(request):
    print('########################################################')
    print('########################################################')
    print('#############    views.index        ####################')
    print('########################################################')
    print('########################################################')
    print('########################################################')

    if request.method == 'POST':
        pass
    else:
        search_form = wiki_search_form()
        return render(request, "encyclopedia/index.html", {
                        'heading': 'All Pages',
                        'search_form': search_form.as_p,
                        "entries": util.list_entries()
        })
# end index




def process_search(request):
    print('########################################################')
    print('########################################################')
    print('##########    views.process_search      ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    
    def find_possible_matches(search_item):
        print(f"Search term = {search_item}")
        
        # Performing a Case Insensitive regex search
        # ie
        # search_term = 'th'
        # lst = ['OTher', 'tHiSTle', 'THIS', 'with']

        # Create a regex pattern with the search term ignoring case
        # pattern = re.compile(search_term, re.IGNORECASE)
        # Use list comprehension to filter the list based on the pattern
        # matching_items = [item for item in lst if re.search(pattern, item)]
        # print(matching_items)
        
        # Create a regex pattern with the search term ignoring case
        pattern = re.compile(search_item, re.IGNORECASE)
        
        # Use list comprehension to filter the list based on the pattern
        results =[entry for entry in wiki_pages if re.search(pattern, entry)]
        match_found = True
        if not results:
            match_found = False
            
        return match_found, results
    #end find_possible_matches
    
    """
        recieves request.POST from form submission
        extract search term from POST
        check reasonable variations of search_term against page list
        if entryfound rredirect to corrosponding page
        else redirect to Not Found Page
    """
    
    wiki_pages = util.list_entries()
    
    wiki_search = request.POST['search_term']
    page_found, wiki_search = util.check_page_exists(request.POST['search_term'])
    """
        At this point wiki_search will contain either
        1. A standardised page name eg they search for 'django' in the form. This is converted to 'Django'
        2. The user search tern wasnt found so wiki_search will get the same value back and be unchanged
    """

    if page_found:
        return HttpResponseRedirect(reverse('encyclopedia:fetch_wiki_page', args=(wiki_search,) ))
    else:
        match_found, entries = find_possible_matches(wiki_search)
        if not match_found:
            heading='Cant find a Wiki for '+wiki_search
            entries.append('Return to Main Page')
            search_form = wiki_search_form(request.POST)
            return render(request, 'encyclopedia/page_not_found.html', {
                        'heading': heading,
                        'search_form': search_form.as_p,
                        'entries': entries,
                        'page_request': wiki_search
            })
        #endif
        
        heading='Search Results'
        search_form = wiki_search_form()
        return render(request, 'encyclopedia/index.html', {
                        'heading': heading,
                        'search_form': search_form.as_p,
                        'entries': entries
        })
#end process_search






def fetch_wiki_page(request, wiki_page):
    """
    get list of all pages
    if requested page is in the list of wiki pagea
        get the markup from the file *** Do this in the template
        convert markup to HTML *** Do this in the template when rendering
        render wiki page
    else
        render not found page
    """
    print('########################################################')
    print('########################################################')
    print('#############    fetch_wiki_page    ####################')
    print('########################################################')
    print('########################################################')
    print('########################################################')


    # check_page_exists: returns page_not_found == True if page not in the entries directory
    # check_page_exists: returns the wiki_page as it is listed in the entries directory ie css will return CSS
    page_found, checked_page = util.check_page_exists(wiki_page)
    print(f'returned to fetch_page_wiki: \npage_found = {page_found}, \nchecked_page = {checked_page}\nrequested page = {wiki_page}')
 
    if page_found:#page exists, so open corrosponding wiki markdown page using the name from the wiki_page_lists
        # wiki_md = util.get_entry(checked_page)
        #covert markdown to html context
        print(f'##################### wiki_page => {wiki_page}',type(wiki_page))
        wiki_page_filename = checked_page + '.md'
        #wiki_html = util.new_markdown_to_html(wiki_md)
        wiki_html = jefmcd2html.translate_md2html(wiki_page_filename)
        print(f'returned to fetch_page_wiki: finished converting md to html')
        print(f'returned to fetch_page_wiki: about to render wiki_page with this content\n{wiki_html}')
        search_form = wiki_search_form()
        wiki_header_title = "<h1>Page Exists</h1>"
        #render the wiki page with the context
        return render(request, "encyclopedia/wiki_page.html", {
                            "wiki_header": wiki_header_title,
                            "wiki_page": checked_page,
                            "wiki_html": wiki_html,
                             "search_form": search_form.as_p
        })
    else: # requested page not found
        heading='Cant find a Wiki for ' + wiki_page
        entries='Return to Main Page'
        search_form = wiki_search_form()
        return render(request, 'encyclopedia/page_not_found.html', {
                    'heading': heading,
                    'search_form': search_form.as_p,
                    'entries': entries,
                    'page_request': wiki_page
        })
    #endif
        
# end fetch_wiki_page
    
    
    
def new_wiki_form(request):
    print('########################################################')
    print('########################################################')
    print('##########    views.new_wiki_form       ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    new_wiki_form = wiki_page_form()
    search_form = wiki_search_form()
    return render(request, 'encyclopedia/load_new_wiki_form.html',{
                    'search_form': search_form.as_p,
                    'create_wiki_form': new_wiki_form.as_p,
                    'wiki_page': 'Create New Wiki'
    })


        
    
#end create_new_wiki

def create_new_wiki(request):
    print('########################################################')
    print('########################################################')
    print('##########    views.create_new_wiki     ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    """
        get the request.POST and capture the wiki title and wiki body
        if page title already exists
            stay on page
            display error message
            allow user to correct error

        create a new file containing the body
        redirect to new page
    """
    title = request.POST['page_title']
    body = request.POST['page_content']
    wiki_search = default_storage.get_valid_name(title)
    # strip whitespaces and special characters from title
    
    # form the path to the target file to be created
    wiki_entries_location = 'entries/'
    wiki_root_path = os.path.dirname('.')
    wiki_entries_path = os.path.join(wiki_root_path, wiki_entries_location)
    target_file = wiki_entries_path + wiki_search + '.md'
    if(os.path.exists(target_file)):
        # If you need to delete file
        # os.remove(target_file)
        new_wiki_form = wiki_page_form(request.POST)
        search_form = wiki_search_form()
        return render(request, 'encyclopedia/load_new_wiki_form.html',{
                'search_form': search_form.as_p,
                'create_wiki_form': new_wiki_form.as_p,
                'wiki_page': 'Create New Wiki:<br> <h3>Title Already Exists. Select another</h3>'
        })
    else:

        new_wiki_file = open(target_file, 'wt')
        new_wiki_file.write(body)
        new_wiki_file.close
        
 
        
    if True:
        return HttpResponseRedirect(reverse('encyclopedia:fetch_wiki_page', args=(wiki_search,) ))
    else:
        return render(request, 'encyclopedia/test.html', {
                        'title': title,
                        'body': body,
                        'valid_title': wiki_search,
                        'wiki_entries_path': wiki_entries_path,
                        'target_file': target_file,
        })
#end create_new_wiki

def edit_wiki(request, wiki_page):
    print('########################################################')
    print('########################################################')
    print('##########    views.edit_wiki           ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    """
        open the corrosponding wiki markdown file
        read contents
        populate a textarea
        save changes when save clicked
        redirect to new page
    """
    entries_path = 'entries/'
    current_dir = os.path.dirname('.')
    target_path = os.path.join(current_dir, entries_path)
    print(f"wiki_page => {wiki_page}")
    
    target_file = wiki_page + '.md'
    target_wiki = os.path.join(target_path, target_file)
    wiki_read_file = open(target_wiki, 'rt')
    wiki_contents = wiki_read_file.read

    from django import forms
    class wiki_edit_form(wiki_page_form):
        page_title = forms.CharField(initial = wiki_page,
                                     widget=forms.TextInput(attrs={
                                        'readonly': True,
                                        'disabled': True
                                     }))
        page_content=forms.CharField(label = '',
                                     initial= wiki_contents,
                                     widget = forms.Textarea)
    
    edit_form = wiki_edit_form()
    search_form = wiki_search_form()
    
    print(f"edit_wiki: wiki_page = {wiki_page}")
    
    return render(request, 'encyclopedia/edit_wiki_page.html', {
                    'wiki_page': wiki_page,
                    'edit_form': edit_form,
                    'search_form': search_form,
                    })
#end edit_wiki

def save_wiki_edit(request, wiki_page):
    print('########################################################')
    print('########################################################')
    print('##########    views.save_wiki_edit      ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    """
        find wiki page in entries directory
        copy current wiki page to a backup file
        delete existing entry
        create new wiki with new content.
        redirect to new file
    """
    
    

    
    #find the target wiki page and make a backup before messing with the original
    

    
    current_dir = os.path.dirname('.')
    entries_dir = 'entries/'
    entries_path = os.path.join(current_dir, entries_dir)
    
    target_wiki = entries_path + wiki_page + '.md'
    target_wiki_backup = jefmcd2html.make_backup_file(target_wiki)
    
    #delete original wiki page and create a new one with the new content
    new_content = str(request.POST['page_content'])
    os.remove(target_wiki)
    new_wiki = open(target_wiki, 'wt')
    new_wiki.write(new_content)
    new_wiki.close
    
    #delete temporary backup page
    print('##################################################')
    print('##################################################')
    print('##################################################')
    
    if os.path.exists(target_wiki_backup):
        print(f'\n\nbackup file {target_wiki_backup} EXISTS\n\nREMOVING\n\n')
        #os.remove(target_wiki_backup)
    else:
        print(f'\n\nbackup file {target_wiki_backup} CANNOT BE FOUND\n\nCANT REMOVE\n\n')
    
    print('##################################################')
    print('##################################################')
    print('##################################################')
    
    #redirect to edited wiki page with the new content
    return HttpResponseRedirect(reverse('encyclopedia:fetch_wiki_page', args=(wiki_page,)))
    
#end save_wiki_edit

def random_wiki(request):
    print('########################################################')
    print('########################################################')
    print('##########    views.random_wiki         ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    import random
    wiki_list = util.list_entries()
    random.shuffle(wiki_list)
    random_wiki = wiki_list[1]
    
    return HttpResponseRedirect(reverse('encyclopedia:fetch_wiki_page', args=(random_wiki,)))
#end random_wiki


