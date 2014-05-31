import urllib
import urllib2
import mechanize
import re
from bs4 import BeautifulSoup 

# Getting Credentials from user
RNO = raw_input("Register No: ")
DOB = raw_input("Date of Birth: ")

# Login to site
print "Hitting the site."
url = 'http://coe1.annauniv.edu/home/index.php'
br = mechanize.Browser()
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10')]
br.open(url)

# Captcha
print "Resolving Captcha.."
soup = BeautifulSoup(br.response().read())
stripper_captcha = soup.find_all('form')[1].contents[3].text[74:95].encode('utf-8')
pat = "\((.*?)\)"
a = re.findall(pat, stripper_captcha)
if a[0].find('+') != -1:
        sympos = a[0].find('+')
        len_str = len(a[0])
        a1 = a[0][0:sympos]
        a2 = a[0][sympos+1:len_str]
        captcha = int(a1)+int(a2)
        captcha = str(captcha)

if a[0].find('-') != -1:
        sympos = a[0].find('-')
        len_str = len(a[0])
        a1 = a[0][0:sympos]
        a2 = a[0][sympos+1:len_str]
        captcha = int(a1)-int(a2)
        captcha = str(captcha) #We got the answer for the captch here in 'captcha'
print "Captcha Resolved..."


# Submitting students login form
print "Filling Students Login form...."
br.select_form(name = "login_stu")
br["register_no"] = RNO
br["dob"] = DOB
br["security_code_student"] = captcha

# After successful submission, We got into the students profile portal now
print "Submitting the form to the server....."
response = br.submit()

# We are navigating to Results tab
print "Entered into Students portal......"
print "Navigating to 'Exam Results' tab......."
br.select_form(name = "formExamResults")
response = br.submit()


# Scrapping results
supersoup = BeautifulSoup(response.read())
print "\nWelcome", supersoup.findAll('th')[3].text.encode('utf-8')
print "\nYahoo! You have logged into the web portal with your credentials and you are now into the 'Exam Marks' section.\n\nPlease feel free to further extend the code like\n-Exceptions when wrong credentials are entered\n-Scrapping the required semester marks\n-Saving them to a .csv\n-Getting a set of credentials from text file and do batch processing etc etc.. :-)\n\nRegards\nVikneshwaren\n"
