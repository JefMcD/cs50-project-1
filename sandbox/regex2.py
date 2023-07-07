import re
import os
import os.path
#################################################################
"""
    Simple markdown2html

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
"""
#################################################################




#################################################################
"""
    Leave the original text string unaltered
    Find the MD tags 
    Extract them
    convert them to HTML
    print out the new tags
"""
#################################################################
text = '#Header1'
text2 = 'A header the is #Delimited text# so be the head of page'
pattern = re.compile(r'(#.+#)|(#\S+)')
matches = pattern.finditer(text2)
for match in matches:
    header_md = match.group()
    print(f"match = {header_md}")
    pattern = re.compile(r'^#')
    header_md = pattern.sub('<h1>', header_md)
    print(f'start substution => {header_md}')
    endhash = re.compile(r'#$')
    if endhash.search(header_md):
        print('endhash found')
        header_html = endhash.sub(r'<\\h1>', header_md)
        print(f'sub endhash => {header_html}')
    else:
        print('endhash not found')
        header_html = header_md + '<\h1>'

    print(f'Final HMTL => {header_html}')
    print(f'Original text => {text2}')
#end for loop


    
###################################################################
"""
    Make the substitution to the original text string
    Find the MD tag
    substitute MD tags for HTML tags in place on original text string
    print new string with new HTML tags
"""
###################################################################
    
bold_text = 'there is a word in **bold** here'
bold_pattern = re.compile(r'(\*{2}.+\*{2})')
matches = bold_pattern.finditer(bold_text)
for match in matches:
    print(match.group())
    newbold = bold_pattern.sub(r'REPLACED', bold_text)
    print(f'bold text => {bold_text}')
    print(f'new bold text => {newbold}')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
emph_text = 'there is *empahis* text here'
emph_pattern = re.compile(r'\*.+\*')
matches = emph_pattern.finditer(emph_text)
for match in matches:
    print(match.group())
          
list_text = 'there is \n*list1 text \n+list2 item \n-list3 item \n and there your go'
list_pattern = re.compile(r'[*+-].+')
matches = list_pattern.finditer(list_text)
for match in matches:
    print(match.group())
    
para_text = 'paragraph1\n\nParagraphs2.\nA paragraph is simply one or more consecutive lines of text, separated by one or more blank lines'
para_pattern = re.compile(r'(.+?\n\n|.+?$)',re.DOTALL)
matches = para_pattern.finditer(para_text)
for match in matches:
    print(match.group())    

