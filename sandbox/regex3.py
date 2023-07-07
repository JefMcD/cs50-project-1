import re

"""
Backslashes in regular expressions are fiendish

I've used a raw string (r'<\\h1>') as the replacement string. 
The 'r' prefix before the string indicates that it should be treated as a raw string literal, 
allowing the backslash to be interpreted correctly as a literal backslash
"""

hashstring = '#heading#'
pattern = re.compile(r'#$')
new_hashstring = pattern.sub(r'<\\h1>', hashstring)

print(new_hashstring)


hashstring2 = '#heading2#'
new_hashstring2 = re.sub(r'#$', r'<\\h1>', hashstring2)

print(new_hashstring2)