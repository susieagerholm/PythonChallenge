from bs4 import BeautifulSoup, Comment
import urllib.request
import re
import pickle
import zipfile
import io
import patoolib
from PIL import Image
from collections import OrderedDict
import string

'''
General to do: Remove all references to concrete URLs in order to prepare code for github :)
Also make sure to comment all parts that might require further understanding...
'''

def get_soup_from_url(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def challenge1():
    print(2 ** 38)

def challenge2(url): 
    soup = get_soup_from_url(url)              			   # input URL
    print(soup.prettify())
    
    my_alphabet = string.ascii_lowercase	               # create input table
    my_output = list(my_alphabet[2:])                 	   # create output table   
    my_output.extend(['a', 'b'])
    
    crypt = soup.find(attrs={'color' : '#f000f0'}).getText()
    res = crypt.translate(str.maketrans(my_alphabet,''.join(my_output)))
    print("TRANSLATE: " + res)
    
    crypt2 = "map"
    res2 = crypt2.translate(str.maketrans(my_alphabet,''.join(my_output)))
    print("URL: " + res2)
    
def challenge3(url):
    soup = get_soup_from_url(url)
    
    res = []
    for my_comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
        res.append(my_comments.extract())
    
    
    result = ""
    for character in res[1]:
        if character.isalpha():
            result = result + character
    
    print(result)

def challenge4(url):
    soup = get_soup_from_url(url)
    
    all_comments = []
    for my_comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
        all_comments.append(my_comments.extract()) 
        
    sub = '[^A-Z]+[A-Z]{3}[a-z][A-Z]{3}[^A-Z]+'
    patterns = re.findall(sub, all_comments[0])
    
    result = ""
    
    for r in patterns:
        clean = re.search('[A-Z]{3}[a-z][A-Z]{3}', r)
        result += (clean.group(0)[3])
        
    print(result)   

def challenge5(url_base, param):
    page = urllib.request.urlopen(url_base + param)
    html = page.read()
    counter = 0    
    my_links = []
    
    while html is not None:
        next = re.findall('the next nothing is [0-9]+', html.decode("utf-8"))
        if len(next) == 0:
            msg = html.decode("utf-8")
            if msg in ["Yes. Divide by two and keep going.", "test"]:
                latest = my_links.pop()                                     # get the latest URL integer
                url = int(latest) / 2                                       # divide by 2
                html = ('the next nothing is ' + str(url)).encode('utf-8')  # encode and fit to pattern
                my_links.append(latest)                                     # append to linked list
            else: 
                print("RESULT URL: " + msg)
                #print (my_links)
                exit()
        else: 
            next.reverse()
            my_pattern = ""
            for my_char in next[0]:
                if my_char.isnumeric():                                     # clean next for all other than numeric char
                   my_pattern = my_pattern + my_char
            my_links.append(my_pattern)                                          # append to linked list
            #print(str(counter) + " : " + my_pattern) 
            url = url_base + my_pattern
            page = urllib.request.urlopen(url)
            html = page.read()  
        counter += 1
                
           
    print("HTML IS NONE")              # failsafe if unexpected input..
    print(my_links)
    exit()
        
def challenge6(url):
    payload = pickle.load( urllib.request.urlopen(url) )
    print (payload)
   
    result = []
    for p in payload:
        my_line = ""
        for pp in p:
            for x in range(0, int(pp[1])):
                my_line = my_line + (pp[0])
        result.append(my_line)    
    
    for line in result:
        print(line) 
        
        
def challenge7(url):
    my_zipper, headers = urllib.request.urlretrieve(url, 'my_zip_file.zip')
    z = zipfile.ZipFile('my_zip_file.zip', 'r')
    print(z.read('readme.txt'))
        
    result = ""
    msg = z.read('90052.txt').decode('UTF-8')
    result = result + z.getinfo('90052.txt').comment.decode('UTF-8')
    
    while 'Next nothing is' in msg:
        no = re.search('[0-9]+', msg)
        my_path = no.group(0) + '.txt'
        msg = z.read(my_path).decode('UTF-8')       
        result = result + z.getinfo(my_path).comment.decode('UTF-8')
    
    print (result)
 
def challenge8(url):
        
    my_img, headers = urllib.request.urlretrieve(url, 'my_image.png')
    
    img = Image.open(my_img) 
    width, height = img.size #Get width and hight as tub
    
    pixels = []
    for x in range (0, width):
        pixels.append(img.getpixel((x, img.height / 2)))
    
    result = ""
    curr = None
    for rbg in pixels:
        if rbg[0] != curr:
            result = result + chr(rbg[0])           # chr() - translate from ASCII code to letter 
            curr = rbg[0]
    
    print(result)
    
	
