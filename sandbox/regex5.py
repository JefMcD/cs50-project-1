
import re

text =" When the Covid Scam kicked off I had a crazy idea that if everybody did what they normaly do as some kind of protest then it would quickly collapse under the weight of public pushback. \n\n\nYou know, like Albert Camus, 'make you very existance be an act of rebellion'. As it unfolded I was dismayed by the grovelling obedience of my fellow man and how they gleefully collaborated with tyranny and absurdity. \n\nI dont think I will ever get over that. You Know? Knowing that horror exists in most people. Well anyway, I have to do something and this is what I got "
text_blocks = re.findall(r'(?s)(?:(?<=\n\n)|^).*?(?=\n\n|$)', text, re.DOTALL)

i = 0
for block in text_blocks:
    print(f">>>>>>>> iter {i}\n")
    print(f'{block}')
    i += 1
