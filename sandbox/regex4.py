

#########################################################################
#########################################################################
"""
    module: jefmcd2html
    markdown to html conversion
    
    called using: 
    from . import jefmcd2hmtl 
    jefmcd2html.translate_md2html(filename)
    
    input: filename eg 'star_trek.md'
    output: str containing html version of the markdown
    
"""
#########################################################################
import re
import os
import os.path
from pathlib import Path
#from django.core.files.storage import default_storage 
#from django.core.files.base import ContentFile

#################################################################
"""
    ruff Pseudo code

    Copy existing Markdown File to a backup file for recovery
    Open target markdown file
    Create new empty markdown2html string
    for each line in Markdown File
        for every possible Markdown tag (A list containing the regex expressions to loop through)
            scan line with regex
            if tag found
                replace md tags in line with html tags
            }
        }
        append line to new markdown2html string
    }
    close taget markdown file
    delete backup markdown file
    return new markdown2html string
    
    
    markdown_tags = ['**', '+', '-', '#', '##', '###']
    
    markdown_regex = ["r'(#.+#)|(#\S+)'",   Header      #
                      '(\*{2}.+\*{2})',     Bold        **
                      '\*.+\*',             emphasis    *
                      '[*+-].+'             list items  + -
                      '(\n.+?\n\n|.+?$)']   paragraph   \n...\n\n
   
    markdown_regex = ['(#.+#)|(#\S+)'] #heading <h1>
"""
#################################################################


def make_backup_file(wiki_page):
    #establish where we are
    original_content = Path(wiki_page).read_text()

    target_wiki_backup = wiki_page + '_backup.txt'
    target_file_backup = open(target_wiki_backup, 'wt')
    target_file_backup.write(original_content)
    target_file_backup.close
    
    return target_wiki_backup
#end make_backup_file


def test_environment(md_file):
    print('############## test_environment ################')
    #establish where we are
    current_dir = os.path.dirname(__file__)
    print(f'current_dir of the file being run => {current_dir}')
    head, tail = os.path.split(__file__)
    print(f'current path head => {head}')
    print(f'current path tail => {tail}')
    abspath, current_dir = os.path.split(head)
    print(f'current_dir => {current_dir}')
    entries_path = 'entries'
    print(f'entries path => {entries_path}')
    print(f'received => {md_file}')
    listing = os.listdir()
    print(f'listing => {listing}')
    if os.path.exists(entries_path):
        print(f'found entries path')
    else:
        print(f'entries not found')
#end new_markdown2html



def parse_tags(line, open_rx, close_rx, markdown_tag, html_open_tag, html_close_tag):
    # eg new_html_line = parse_h2_tags(new_html_line, '(?<!\*)\*\*(?=\w)', '(?<=\w)\*\*(?!\*)' '##', '<h2>','</h2>'
    #   match for header tag #inline delimited tag# or #singletag
    """
    bold_open_mdtag_rx = '(?<!\*)\*\*(?=\w)'
    bold_close_mdtag_rx = '(?<=\w)\*\*(?!\*)'
    bold_md_tag = '\*\*'
    """
    print(f'************* parse_tags *****************')
    print(f'recieved:\nline = {line}\nopen_rx => {open_rx}\nclose_rx => {close_rx}\nmarkdown_tag => {markdown_tag}\nhtml_open_tag => {html_open_tag}\nhtml_close_tag => {html_close_tag}')
    new_html_line = line
    md_tag_pattern = re.compile(rf'{open_rx}')
    matches = md_tag_pattern.finditer(line)
    for match in matches:
        header_md = match.group()
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> match = {header_md}")
        
        #if opening tag at start of line substitute standard <x> 
        starthash = re.compile(rf'^{markdown_tag}')
        if starthash.search(line):
            new_opentag_line = starthash.sub(html_open_tag, line)
        else:
            #opening tag inline - insert a space before <x>
            starthash = re.compile(rf'\s{html_close_tag}')
            new_opentag_line = starthash.sub(html_close_tag, line)
        
        # changes are incremental one step at a time, so save changes to line
        line = new_opentag_line
        
        # mixing single tags with double tags on the same lines causes the double tags to have no opening tag, so...
        # sooo... this hack replaces loose opening tags with an <x>
        # >>> This is a misunderstanding of HTML. A header tag automatically creates a newline so you cant have two seperate H2 etc on the same line
        loosehash = re.compile(rf'\s{markdown_tag}')
        new_opentag_line = loosehash.sub(f' {html_open_tag}', line)
        

        
        # process closing tag
        endhash = re.compile(rf'{close_rx}') # em close_rx = '</em> '
        if endhash.search(new_opentag_line):
            print('endhash found')
            new_html_line = endhash.sub(html_close_tag, new_opentag_line)
            print(f'sub endhash => {new_html_line}')
        else:
            #find the header tag and close the white space at the end with a </x> 
            print('endhash not found')
            end_nl = re.compile(r'\n$')
            html_close_tag = html_close_tag+'\\n'
            new_html_line = end_nl.sub(html_close_tag, new_opentag_line)
            print(f'new_html_line => {new_html_line}')

        print(f'Final HMTL => {new_html_line}')
        
    #end matches for loop

    return new_html_line 
#end parse_tags


def parse_ul_tags(line, open_rx, markdown_tag, html_open_tag, html_close_tag, first_li_flag):
    # new_html_line = parse_h2_tags(new_html_line, '(^[+-].*)', '[+-]', '<li>','</li>'
    #   match md list tag at beginning of line
    print(f'************* parse_ul_tags *****************')
    print(f'recieved:\nline = {line}\nopen_rx => {open_rx}\nmarkdown_tag => {markdown_tag}\nhtml_open_tag => {html_open_tag}\nhtml_close_tag => {html_close_tag}')
    new_html_line = line
    md_tag_pattern = re.compile(rf'{open_rx}')
    matches = md_tag_pattern.finditer(line)
    for match in matches:
        header_md = match.group()
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> match = {header_md}")
        
        #li tag must be at start of line so substitute standard <li> and close line with </li>\n 
        starthash = re.compile(rf'^{markdown_tag}')
        if starthash.search(line):
            new_opentag_line = starthash.sub(html_open_tag, line)
        
        # changes are incremental one step at a time, so save changes to line
        line = new_opentag_line
        print(f'first sub done line => {line}')
        # process closing tag
        endhash = re.compile(r'\n$')
        new_html_line = endhash.sub(r'</li>\n', line)

        print(f'Final HMTL => {new_html_line}')
        
    #end matches for loop

    if first_li_flag == True:
        new_html_line = "<ul class='wikipage_list'>"+new_html_line
        first_li_flag = False
    return first_li_flag, new_html_line 
#end parse_ul_tags



"""
    strip_brackets_from_parenthesis
    
    input: strip_brackets_from_parenthesis(md_link, pattern, left_regex, right_regex):
    
                md_link: eg [an example](http://example.com/ "Title")
                text_pattern eg re.compile(r'\[.+\]')
                left_regex: eg '\['
                right_regex: eg '\]'
                
    returns:  the text inside the parenthesis eg 'for example'
    
    This is a general use function for returning the contents of parenthesis used in markdown links
    It is a general use version of the following code used for removing parenthesis, since it is a common task
     
            link_text_matches = text_pattern.finditer(md_link) # text_pattern matches the text link part eg [for example]
            for link_match in link_text_matches:
                link_text = link_match.group()
                left_pattern = re.compile(r'\[')
                text_link_lgone = left_pattern.sub('',link_text)
                right_pattern = re.compile(r'\]')
                md_link_text = right_pattern.sub('',text_link_lgone)
            print(f'link_text => {raw_link_text}')
"""
def strip_brackets_from_parenthesis(md_link, pattern, left_regex, right_regex):
    
    stripped_parenthesis_list = []
    matches = pattern.finditer(md_link) # pattern matches the parenthesis pattern eg matches [for example]
    for match in matches:
        parenthesis = match.group() # assigns match value eg parenthesis = [for example]
        left_brkt_pattern = re.compile(rf'{left_regex}') # match left bracket
        parenthesis_lgone = left_brkt_pattern.sub('',parenthesis) # remove left bracket
        right_brkt_pattern = re.compile(rf'{right_regex}') # match right bracket
        stripped_parenthesis = right_brkt_pattern.sub('',parenthesis_lgone) #remove right bracket
        stripped_parenthesis_list.append(stripped_parenthesis) # add result to list
    #endfor
    return stripped_parenthesis_list
#end strip_brackets_from_string


def parse_link_tags(line):
    """
        for regex lookaheads https://stackoverflow.com/questions/2973436/regex-lookahead-lookbehind-and-atomic-groups
        
        input: line -> a string of the format 
                            [an example](http://example.com/ "Title")
                            [This link](http://example.net/)
                            [About](/about/)
                            
        output: html -> a string of the format
                            <a href='http://example.com/' title='Title'>an example</a>
                            <a href='http://example.net/'>This link</a>
                            <a href='/about/'>About</a>
                            
        Markdown Reference Links Not Supported - FTN
        
        So the square brackets contain the link text
        and the round brackets contain the url text
        
        regex for link text => r'(\[.+\]) 
        if empty create a default value = 'click'
        
        regex for url text => r'(\(.+)\))
        if empty create default value = '#'
        
        ruff Pseudo Code
        if line contains a link
            process link
            return html
        else
            return line unaltered
    """
    # check if line contains a link
    link_pattern = re.compile(r'\[.+\]\(.+\)') # anchor tag or img tag

    if link_pattern.search(line):
        # process link
        
        print(f'*************** parse_link_tags *****************')
        print(f'input line : {line}')
        #find link_text
        raw_link_text = []
        text_pattern = re.compile(r'\[(.*?)\]') #usual characters for writinf (.*) doesnt work if theres more than two links on a line
        text_regex = '\[(.*?)\]'
        
        raw_url_link = []
        url_pattern = re.compile(r'\((.*?)\)') # same character set but for url markdown part ([...])
        url_regex = '\((.*?)\)'
        
        full_link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
        
        ## There must be a better way of doing this ???? but this'll get the job done in the meantime
        
        matches = link_pattern.finditer(line)
        i=1
        for match in matches:
            print(f'\n\n>>>>>>>> iteration => {i} >>>>>>>>>>>> {i} >>>>>>>>>>>>>>> {i}\n')
            md_link = match.group() #contains full md_link eg [an example](http://example.com/ "Title")
            print(f'Finding Text markdown link => {md_link}')
            
            # strip brackets and assign the md_link text value to a variable
            raw_link_text = strip_brackets_from_parenthesis(md_link, text_pattern, '\[', '\]') # returns the link text eg 'for example'
            print(f"\nparse_link_tags: raw_link_text => {raw_link_text}\\n, count = {len(raw_link_text)}")
            
            raw_url_link = strip_brackets_from_parenthesis(md_link, url_pattern, '\(', '\)') # returns the link url eg 'http://example.com/'
            print(f"\nparse_link_tags: raw_url_link => {raw_url_link}\\n, count = {len(raw_url_link)}")
            
            # now we have
            # a list containing the url_text value and
            # a list containing the url_link value

            # match them together in their html urls
            html_urls = []
            count = len(raw_url_link)
            i=0
            while i < count:
                print(f'PASS {i} link => {raw_url_link[i]}\n')
                print(f'PASS {i} raw_link_text => {raw_link_text[i]}\n')
                html_urls.append(f"<a href='{raw_url_link[i]}'>{raw_link_text[i]}</a>")
                print(f'parse_link_tags: html_urls => {html_urls[i]}')
                i = i + 1
            #endwhile
            
            #Now we have a list containing the urls that are contained within the line
            # Next step is to substitute the html for the md tags
            """
                we have the original line 
                eg This is a [an example1](http://example1.com/) of a link this is [another link](http://website.com/) well
                
                and we have the list containing the html
                eg ["<a href='http://example1.com/'>an example1</a>", "<a href='http://website.com/'>another link</a>"]
                
                In the following code
                In this code, we define a regular expression pattern that matches the Markdown links using capture groups. 
                Then, we define a replacement function replace_link() that checks if the link from the list matches the 
                captured link text and URL. If a match is found, the function returns the corresponding HTML link. 
                Finally, we use re.sub() to replace the Markdown links in the string with the HTML links using the pattern 
                and the replacement function.
            """
            print(f'{html_urls}')
            def replace_link(match):
                link_text = match.group(1)
                link_url = match.group(2)
                for html_link in html_urls:
                    if link_text in html_link and link_url in html_link:
                        return html_link

            # Use re.sub() with the pattern and the replacement function to replace the links
            link_pattern = r'\[(.*?)\]\((.*?)\)'
            new_string = re.sub(link_pattern, replace_link, line)
            print(f'new_string = {new_string}')
            #endfor

        return new_string
    else:        
        #no link found
        return line
#end parse_link_tags



def translate_md2html(md_file):
    print('############## jefmcd2html ################')
    #establish where we are
    current_dir = os.path.dirname('.')
    entries = 'entries/'
    entries_path = os.path.join(current_dir, entries)
    target_md_file = os.path.join(entries_path, md_file)
    
    #check target exists
    if os.path.exists(target_md_file):
        print(f'target file exists => {target_md_file}')
    else:
        print(f'cant find => {target_md_file} exiting')
        return
        
    #copy target md_file to a backup for recovery
    backup_target = make_backup_file(target_md_file)
    
    #open target markdown file in read mode
    markdown_file = open(target_md_file, 'rt')
    
    #create new empty new_markdown2html string
    new_markdown2html = str()



    #iterate through markdown file one line at a time
    # https://docs.python.org/3/tutorial/inputoutput.html
    processing_ul = False
    processing_para = False
    
    #bold_open_mdtag_rx = '(\*{2}.+\*{2})'
    #bold_close_mdtag_rx = '(\*\*$)|(\*\*\s)'
    #h2_open_mdtag_rx = '(##.+##)|(##.*)'
    #h2_close_mdtag_rx = '(##$)|(##\s)'
    
    h3_open_mdtag_rx = '(?<!###)###(?=.*)'
    h3_close_mdtag_rx = '(?<=\w)###(?!###)'
    h3_md_tag = '###'
    
    h2_open_mdtag_rx = '(?<!##)##(?=.*)'
    h2_close_mdtag_rx = '(?<=\w)##(?!##)'
    h2_md_tag = '##'
    
    h1_open_mdtag_rx = '(?<!#)#(?=.*)'
    h1_close_mdtag_rx = '(?<=\w)#(?!#)'
    h1_md_tag = '#'
    
    bold_open_mdtag_rx = '(?<!\*)\*\*(?=\w)'
    bold_close_mdtag_rx = '(?<=\w)\*\*(?!\*)'
    bold_md_tag = '\*\*'
    
    em_open_mdtag_rx = '(?<!\*)\*(?=\w)'
    em_close_mdtag_rx = '(?<=\w)\*(?!\*)'
    em_md_tag = '\*'
    
    for line in markdown_file:
        print(f'******* current line ****** => {line}', end='')

        #check line for all markdown tags and perform corrosponding substitution of html for md
        new_html_line = line
        
        # parse_tags(line, open_regex, close_regex, markdown_tag, html_open_tag, html_close_tag):
        new_html_line = parse_tags(new_html_line, h3_open_mdtag_rx, h3_close_mdtag_rx, h3_md_tag, '<h3>','</h3> ') # triple # -> <h3></h3>
        new_html_line = parse_tags(new_html_line, h2_open_mdtag_rx, h2_close_mdtag_rx, h2_md_tag, '<h2>','</h2> ') # double # -> <h2></h2>
        new_html_line = parse_tags(new_html_line, h1_open_mdtag_rx, h1_close_mdtag_rx, h1_md_tag, '<h1>','</h1> ')       # single # -> <h1></h1>
        new_html_line = parse_tags(new_html_line, bold_open_mdtag_rx, bold_close_mdtag_rx, bold_md_tag, '<b>', '</b> ') # ** -> <b></b>
        new_html_line = parse_tags(new_html_line, em_open_mdtag_rx, em_close_mdtag_rx, em_md_tag, '<em>', '</em> ') # * -> <em></em>
        new_html_line = parse_link_tags(new_html_line)
        print(f'>>>>>>>>>>>>>>>> TAGS => new_html {new_html_line}')
        """
            Next we process Unordered List
            The unordered list spans across several lines so we need to keep track of the fact that 
            we are processing an UL or if we have reached the end
            
            When we find a list item tag we set processing_ul = true
            we find lines beginning with + or - minus tags and convert them to <li>
            when we find a line that is not a + or - we have reached the end of the ul processing
            so if processing_ul = true and we find then find anythin other than + or - at the start of the line 
            then that signals its the end of the ul
                        
            Ruff peuedo code;
            if tag is an unordered list
                processing UL = True
                if first item 
                    set first item flag = true
                    pars_tags(li, first_item = true)
                    set first item flag = false
                else
                    parse_tags(li, first_item = false)
            else
                if processing UL = True
                    add UL closing tag </ul>
        """

        ul_pattern = re.compile(r'^[+-].*')
        if ul_pattern.search(new_html_line):
            print(f'*************** found ul')
            
            if processing_ul == False:
                processing_ul = True
                first_li_flag = True
            #endif
            #on first time first_li_flag set to true so prcessing can check if this is the first tag
            # then it adds <ul> tag to front and sets first_li_flag to false
            first_li_flag, new_html_line =  parse_ul_tags(new_html_line, '(^[+-].*)', '[+-]', '<li>', '</li> ',first_li_flag) # * -> <li></li>
        else:
            if processing_ul:
                #end of item list reached
                #replace closing \n with <./ul>\n
                closing_nl = re.compile(r'\n$')
                new_html_line = closing_nl.sub(r'</ul>\n',new_html_line)
                processing_ul = False
                print(f'ul => {new_html_line}')
            # endif
        #endif
        # End Processing Ul Block
        
        # Some html tags are block tags so they come with their own Newline h1, h2 etc, ul, div, p
        # Some are inline tags and do not come with their own newline <b>, <em> <a>
        """
            This part deals with the line breaks and adds them where necessary so that the html matches the markdown
            changes made to default HTML behaviour are thus;
            + header tags restyled to be inline-block so that they dont drop an addition line break. 
              This might be requirements breaking since it diverges from standard markdown, but it also allows more than one tag on a line
            + <ul> tags drop a line break of their own so they dont get the <br> added at the end of the line processing
            + <p> tags are dealt with outside this loop. They drop a <br> of their own
            + <b> tags need a <br> added to the end of the line
            + <em> tags need a <br> added to the end of the line
        """
        
        # Add break to the end of the line ul spans several line so we skip that one until its finished processing the ul
        inline_tags = re.compile(r'(<b>)|(<em>)|(<h1>)|(<h2>)|(<h3>)') 
        block_tags = re.compile(r'(</ul)|(</li>)')
        if not block_tags.search(new_html_line): # If line contains an inline tag
            new_html_line = new_html_line + '<br>'
        
        new_markdown2html = new_markdown2html + new_html_line
        print(f'jefmcd2Html =>\n{new_markdown2html}')
    #end read filelines loop


    """
        Next we process Paragraphs
        
        At this point all the lines have been processed and the corrosponding HTML has been created
        
        the markdown creators define a paragaraph thus:
        'A paragraph is identified as series of lines beginning with a newline and ending with a double newline'
        
        By my interpretation this definition means that everything is contained within paragraphs.
        I want to tighten this definition  a little by specifing the the first line 
        (which may not necessarily begin with a newline) as also being within a paragrah - why not?
        
        This seems to be a little pointless since I will have to redefine the <p> tag so that it doesnt add any 
        extra lines but (on the surface) it appears relatively straightforward. The best way to do this maybe to treat the file as a 
        single entity rather than one line at a time, and change start and end tags globally
        
        ruff Pseudo Code:
        
        match blank line
        match nl at end of a string followed by a nl on a blank line
        
        
        
        
        
        ##############################################################
    """

    text_blocks = re.findall(r'(?s)(?:(?<=\n\n)|^).*?(?=\n\n|$)', new_markdown2html, re.DOTALL)

    i = 0
    for block in text_blocks:
        print(f">>>>>>>> iter {i}\n")
        print(f'{block}')


    print('########################################################')
    print('########################################################')
    print('FINAL HTML\n')
    print(f'{new_markdown2html}')        
   
    #remove temporary backup file
    if os.path.exists(backup_target):
        print(f'Removing Backup file {backup_target}')
        os.remove(backup_target)
    else:
        print(f'cant find {backup_target}')
    #return(new_markdown2html)
#end translate_md2html




#test_environment('ZZ.md')
translate_md2html('mixed_markup.md')



























"""
def parse_header_tags(line):
    #   match for header tag #inline delimited tag# or #singletag
    # This is the function that the general parse_tags() function is based on
    # It containst the workings hard coded for the markup to html for the h1 tag 
    # Hopefully makes it easier to follow
    new_html_line = line
    md_tag_pattern = re.compile(r'(#.+#)|(#\S+)')
    matches = md_tag_pattern.finditer(line)
    for match in matches:
        header_md = match.group()
        print(f"match = {header_md}")
        
        #if opening tag at start of line substitute standard <h1> 
        starthash = re.compile(r'^#')
        if starthash.search(line):
            new_opentag_line = starthash.sub('<h1>', line)
        else:
            #opening tag inline - insert a space before <h1>
            starthash = re.compile(r'\s#')
            new_opentag_line = starthash.sub(' <h1>', line)
        
        # changes are incremental one step at a time, so save changes to line
        line = new_opentag_line
        
        # mixing single tags with double tags on the same lines causes the double tags to have no opening tag, so...
        # sooo... this hack replaces loose opening tags with an <h1>
        loosehash = re.compile(r'\s#')
        new_opentag_line = loosehash.sub(' <h1>', line)

        # process closing tag
        endhash = re.compile(r'(#$)|(#\s)')
        if endhash.search(new_opentag_line):
            print('endhash found')
            new_html_line = endhash.sub(r'<\\h1> ', new_opentag_line)
            print(f'sub endhash => {new_html_line}')
        else:
            #find the header tag and close the white space at the end with a </h1> 
            print('endhash not found')
            end_nl = re.compile(r'\n$')
            new_html_line = end_nl.sub(r'<\\h1>\n', new_opentag_line)
            print(f'new_html_line => {new_html_line}')
        print(f'Final HMTL => {new_html_line}')
    #end matches for loop

    return new_html_line
#end parse_header_tags

"""

#################################################################################
"""
    end of jefmcd2html
"""
#################################################################################


