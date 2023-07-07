import re

from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage
#import markdown2




def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename) 
                                for filename in filenames if filename.endswith(".md"))) 



def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    
    
#def markdown_to_html(md_obj):
    """
       md_obj is the contents of the markdown file
       its of type (str)
       process file and replace markdown with corrosponding html!
            
    """
   # return markdown2.markdown(md_obj)
# end markdown_to_html

#def new_markdown_to_html(md_obj):
    """
       md_obj is the contents of the markdown file
       its of type (str)
       process file and replace markdown with corrosponding html!
            
    """
   # return markdown2.markdown(md_obj)
# end new_markdown_to_html



def check_page_exists(wiki_page):
    print('########################################################')
    print('########################################################')
    print('########    util.check_page_exists      ################')
    print('########################################################')
    print('########################################################')
    print('########################################################')
    # check page name against reasonable variants
    # essentially makes a search case insensitive 
    # found a better way of doing an Ignore case search using regex but left this in just for fun
    """
        #   check_page_exists
        #   input:      wiki_page ie 'css'
        #   returns:    page_not_found == True if page not in the entries directory
        #   returns:    wiki_page as it is listed in the entries directory ie css will return CSS
    """

    request_variants = []
    request_variants.append(wiki_page.capitalize())
    request_variants.append(wiki_page.upper())
    request_variants.append(wiki_page.lower())
    
    # test for reasonable variants of the page name all uppercase, lowercase and capitalised case

    # find the page
    # this has weird behaviour
    # page_exists = [page for page in wiki_page_list if (page_request_capitalize or page_request_lower) == page]
    
    # find the requested page
    
    wiki_page_list = list_entries()
    return_page = wiki_page #If no match found then the wiki_page search term is returned unaltered

    wiki_exists = re.compile(rf'{wiki_page}', re.IGNORECASE)
    matches = wiki_exists.finditer(wiki_page)
    for match in matches:
        test1 = match.group()
        print(f'match found test1 => {test1}')
        print(f'wiki_page to find => {wiki_page}')
    
    for page in wiki_page_list: # iterate through all pages in the list
        """
            check if requested page is in the list
            this is not as simple as it sounds
        
            the match will be true if a subset of the string exists
            ie match will be true for cs matching with css
            so to be sure its the same the length of the two strings should also be the same
        """
        if wiki_exists.match(page):
            if len(page) == len(wiki_page):   
                print(f'found requested page {page}\nreturning return_page => {return_page}\nreturning status => True')     
                return_page = page #return page from list ie if search if for css return CSS
                return True, return_page
            else:
                return False, return_page
        # endif
    # end for
    
    # this will execute only if the page hasnt been found in the list entries
    return False, wiki_page
#end check_page_exists



