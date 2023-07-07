import re

print('old\new\too\run\filr\broop')
print('old\\new')
print(r'old\new\too\run\filr')

# the r prefix causes the string special characters to be treated as normal characters - a raw string
# otherwise special characters need to be escaped if you wan them to be normal charavters
# it has no effect on regex special characters only \n \t \r \f

print('\n \t \r \f')
print(r'\n \t \r \f')

print('\s\w\d')
print(r'\s\w\d')

# Its standard practice to work with the raw string to avoid conflicts with the regex compiler and avoid some confusion


query = "hello bike 765 cover 709 pipe dam soldier 365"
pattern = re.compile(r'\d\d\d') # 3 match consecutive numbers
result = pattern.search(query)
value = int(result.group())
print(value, value+10, type(value))

p = re.compile(r'\b(\w+)\s+\1\b')
double = p.search('Paris in the the spring')
if double:
    print(double.group())
else:
    print(" no doubles")
    
query = 'I am #Header# text'
header_pattern = re.compile(r'#\w+#')
header = header_pattern.search(query)
if header:
    print(header.group())
    md = str(header.group())
    print(md)
    starthash_pattern = re.compile(r'^#')
    starthash = (starthash_pattern.search(md)).group()
    print(starthash)
    endhash_pattern = re.compile(r'#$')
    endhash = (endhash_pattern.search(md)).group()
    print(endhash)
else:
    print('no header')
    

text = '#Header1 on its own needs to be on a single line\nA header the is #Delimited text# so be the head of page'
pattern = re.compile(r'(#.+#)|(#\S+)')
matches = pattern.finditer(text)
for match in matches:
    header_md = match.group()
    print(f"match = {header_md}")
    pattern = re.compile(r'^#')
    header_md = pattern.sub('<h1>', header_md)
    print(f'start substution => {header_md}')
    pattern = re.compile(r'1$')
    if pattern.search(header_md):
        print('end # found')
    else:
        print('end # not found')
    header_md = pattern.sub('</h1>', header_md)
    print(f'end substitution => {header_md}')
    

bold_text = 'the is a **word** in bold here'
bold_pattern = re.compile(r'(\*\*.+\*\*)')
matches = bold_pattern.finditer(bold_text)
for match in matches:
    print(match.group())
    
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

