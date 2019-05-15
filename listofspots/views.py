###################################################
## Recovery Spots is a Blogger Blog that I wrote. It contains, at this writing, 237 Recovery International tools.
# Each post (each tool) contents is just a sentence or two long.
# Each post has no title, which means that Blogger has assigned it one.
# The blog works with javascript to allow the end user to click and see a random tool.
# The purpose of this app is to retrieve all the tools from blogger and try various views
###################################################
from django.shortcuts import render
from bs4 import BeautifulSoup
import json


###################################################
# VIEW HOME
# This is the index page of the app. It shows a list of selections of views
###################################################
def home(request):
    return (render(request, 'index.html'))


###################################################
# VIEW GETPOSTCONTENTS
# This view retrieves all the tools from blogger and displays them.
# It does that by using the Google Blogger API to get the blog.
# The API results in a JSON format
# In the JSON is a variable totalItems that tells me the total number of posts
# Then in a loop, I'm retrieving all the postids from the JSON
# Inside the loop, I construct an api request call based on each post id, then parse it with BeautifulSoup
# to retrieve the tool, which I then append to an ever-growing list.
# After the loop is over, I have a long list of all the tools
# This version also includes a try and except. At first, I couldn't make it fail.
# Then research showed that not all requests non-200 status codes will produce an exception
# Below is the solution I found.
# Important finding about requests and timeouts:
# The timeout value will be applied to both the connect and the read timeouts. Specify a tuple if you would like to set the values separately, such as:
# r = requests.get('https://github.com', timeout=(3.05, 27)) (connect,read)
###################################################
def getpostcontents(request):
    maxposts=5
    blogid='4141263554814875358'
    apikey='AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc'

    url = "https://www.googleapis.com/blogger/v3/blogs/" + blogid + "?maxPosts=" +str(maxposts) + "&view=READER&fields=posts(items%2FselfLink%2CtotalItems)&key=" + apikey
    import requests
    try:
        r  = requests.get(url, timeout=(6.0, 6.0))  # This results in JSON
    except requests.exceptions.ConnectTimeout as e:
        return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
        # test: connect time as first element of tuple
    except requests.exceptions.ReadTimeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
        # test: short connect time as 2nd element of tuple
    except requests.exceptions.Timeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
        # test: no tuple, just put in a short time
    except requests.exceptions.ConnectionError as e:
        return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
        # test: disconnect from internet
    except requests.exceptions.TooManyRedirects as e:
        return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
        # test: ?

    try:
        r.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
        return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})


    j = json.loads(r.text)
    totalitems = (j['posts']['totalItems']) # Here is the total number of posts

    i = 0
    tool_list = []
    while i< totalitems and i < maxposts: # Google blogger API allows a max of 500
        postid=(((j['posts']['items'][i])['selfLink'])[70:89]) # pulls out just the post id
        # construct a requests.get for each postid because I want the content, not the id
        url = "https://www.googleapis.com/blogger/v3/blogs/4141263554814875358/posts/" + str(
            postid) + "?fields=content&key=AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc"
        try:
            r = requests.get(url, timeout=(6.0, 6.0))
        except requests.exceptions.ConnectTimeout as e:
            return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
            # test: connect time as first element of tuple
        except requests.exceptions.ReadTimeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
            # test: short connect time as 2nd element of tuple
        except requests.exceptions.Timeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
            # test: no tuple, just put in a short time
        except requests.exceptions.ConnectionError as e:
            return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
            # test: disconnect from internet
        except requests.exceptions.TooManyRedirects as e:
            return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
            # test: ?
        try:
            r.raise_for_status()  # will raise a HTTPError if the HTTP req returned an unsuccessful status code
        except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
            return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})

        k = json.loads(r.text)
        soup = BeautifulSoup(k['content'], 'html.parser') # Content has only HTML so I get away with BeautifulSoup
        somehtml = soup.find("span").text
        tool_list.append(somehtml) # create a list of all the recovery tools
        i+=1
    return render(request, 'getpostcontents.html', {'allofit':tool_list, 'count':totalitems})

###################################################################################
# def puttoolsinamodel
# this view repeats the above view but instead of displaying the list, it will put the list
# of tools in a model
# In this view, it all goes into one model record as a single string
###################################################################################
def puttoolsinamodel(request): # this gets the tools and puts them in a model
    maxposts = 5
    blogid = '4141263554814875358'
    apikey = 'AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc'

    url = "https://www.googleapis.com/blogger/v3/blogs/" + blogid + "?maxPosts=" + str(
        maxposts) + "&view=READER&fields=posts(items%2FselfLink%2CtotalItems)&key=" + apikey
    import requests
    try:
        r = requests.get(url, timeout=(6.0, 6.0))  # This results in JSON
    except requests.exceptions.ConnectTimeout as e:
        return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
        # test: connect time as first element of tuple
    except requests.exceptions.ReadTimeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
        # test: short connect time as 2nd element of tuple
    except requests.exceptions.Timeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
        # test: no tuple, just put in a short time
    except requests.exceptions.ConnectionError as e:
        return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
        # test: disconnect from internet
    except requests.exceptions.TooManyRedirects as e:
        return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
        # test: ?

    try:
        r.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
        return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})

    j = json.loads(r.text)
    totalitems = (j['posts']['totalItems'])  # Here is the total number of posts
    i = 0
    newstring=" "
    while i < totalitems and i < maxposts:  # Google blogger API allows a max of 500
        postid = (((j['posts']['items'][i])['selfLink'])[70:89])  # pulls out just the post id
        # construct a requests.get for each postid because I want the content, not the id
        url = "https://www.googleapis.com/blogger/v3/blogs/4141263554814875358/posts/" + str(
            postid) + "?fields=content&key=AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc"
        try:
            r = requests.get(url, timeout=(6.0, 6.0))
        except requests.exceptions.ConnectTimeout as e:
            return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
            # test: connect time as first element of tuple
        except requests.exceptions.ReadTimeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
            # test: short connect time as 2nd element of tuple
        except requests.exceptions.Timeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
            # test: no tuple, just put in a short time
        except requests.exceptions.ConnectionError as e:
            return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
            # test: disconnect from internet
        except requests.exceptions.TooManyRedirects as e:
            return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
            # test: ?
        try:
            r.raise_for_status()  # will raise a HTTPError if the HTTP req returned an unsuccessful status code
        except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
            return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})

        k = json.loads(r.text)
        soup = BeautifulSoup(k['content'], 'html.parser') # Content has only HTML so I get away with BeautifulSoup
        thetool = soup.find("span").text
        i += 1
        newstring="<li>" + thetool + "</li>" + newstring

    newstring= "<ol>" + newstring + "</ol>"
    from .models import Recoverytools
    mytools = Recoverytools(rectools=newstring)
    Recoverytools.objects.all().delete()  # delete what was there
    mytools.save('rectools')  # This performs a SQL insert
    return render(request, 'puttoolsinamodel.html', {'allofit': newstring, 'count':totalitems})
####################################################
# Now retrieve the tools from the model and display them
# This view pulls out the one long record from the model that contains all the stored tools
####################################################
def show_the_model_data(request):
    from .models import Recoverytools
    instance = Recoverytools.objects.values_list('rectools', flat=True).distinct()

    return render(request, 'show_the_model_data.html', {'allofit': instance[0]})
    # I only need record zero from instance because the entire string is in one record

###################################################################################
###################################################################################
###################################################################################
###################################################################################
# def bulkstoretoolsinamodel
# this view bulk stores the tools in a model   #
###################################################################################
def bulkstoretoolsinamodel(request): # this gets the tools and puts them in a model
    maxposts = 500
    blogid = '4141263554814875358'
    apikey = 'AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc'

    url = "https://www.googleapis.com/blogger/v3/blogs/" + blogid + "?maxPosts=" + str(
        maxposts) + "&view=READER&fields=posts(items%2FselfLink%2CtotalItems)&key=" + apikey
    import requests
    try:
        r = requests.get(url, timeout=(6.0, 6.0))  # This results in JSON
    except requests.exceptions.ConnectTimeout as e:
        return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
        # test: connect time as first element of tuple
    except requests.exceptions.ReadTimeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
        # test: short connect time as 2nd element of tuple
    except requests.exceptions.Timeout as e:
        return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
        # test: no tuple, just put in a short time
    except requests.exceptions.ConnectionError as e:
        return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
        # test: disconnect from internet
    except requests.exceptions.TooManyRedirects as e:
        return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
        # test: ?

    try:
        r.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
        return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})

    j = json.loads(r.text)
    totalitems = (j['posts']['totalItems'])  # Here is the total number of posts
    i = 0
    newstring=" "
    from .models import Recoverytoolsbulk
    if Recoverytoolsbulk.objects.all() != {}:
            Recoverytoolsbulk.objects.all().delete()  # delete what was there
    instances=[]
    while i < totalitems and i < maxposts:  # Google blogger API allows a max of 500
        postid = (((j['posts']['items'][i])['selfLink'])[70:89])  # pulls out just the post id
        # construct a requests.get for each postid because I want the content, not the id
        url = "https://www.googleapis.com/blogger/v3/blogs/4141263554814875358/posts/" + str(
            postid) + "?fields=content&key=AIzaSyDLDo-nCeC28cYW6gvIz3t38U_5m_6gcFc"
        try:
            r = requests.get(url, timeout=(6.0, 6.0))
        except requests.exceptions.ConnectTimeout as e:
            return render(request, 'error.html', {'errormsg': "LM: Connection Timeout", 'errorcode': e})
            # test: connect time as first element of tuple
        except requests.exceptions.ReadTimeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Read Timeout', 'errorcode': e})
            # test: short connect time as 2nd element of tuple
        except requests.exceptions.Timeout as e:
            return render(request, 'error.html', {'errormsg': 'LM: Unknown Timeout', 'errorcode': e})
            # test: no tuple, just put in a short time
        except requests.exceptions.ConnectionError as e:
            return render(request, 'error.html', {'errormsg': 'LM: Connection Error', 'errorcode': e})
            # test: disconnect from internet
        except requests.exceptions.TooManyRedirects as e:
            return render(request, 'error.html', {'errormsg': 'LM: Too Many Redirects', 'errorcode': e})
            # test: ?
        try:
            r.raise_for_status()  # will raise a HTTPError if the HTTP req returned an unsuccessful status code
        except requests.exceptions.HTTPError as e:  # test: add an exclamation mark to end of key
            return render(request, 'error.html', {'errormsg': 'HTTP Bad Status Code', 'errorcode': e})

        k = json.loads(r.text)
        soup = BeautifulSoup(k['content'], 'html.parser')
        # Content has only HTML so I get away with BeautifulSoup
        thetool = soup.find("span").text
        instances.insert(i, Recoverytoolsbulk(rectoolsbulk = thetool ))
        i += 1

    # bulk_create creates a dictionary
    thedictionary=Recoverytoolsbulk.objects.bulk_create(instances)
    return render(request, 'bulkstoretoolsinamodel.html', {'allofit': thedictionary, 'count':totalitems})
####################################################
# Now retrieve the bulk stored tools from the model and display them. It uses in_bulk
# to retrieve all the tools at the same time
####################################################
def show_the_model_data_bulk_stored(request):
    from .models import Recoverytoolsbulk
    mystring=""
    allthetools = Recoverytoolsbulk.objects.in_bulk()
    # in_bulk produces a standard Python dictionary

    for tool in allthetools.values():
        mystring="<li>" + str(tool) + "</li>" + mystring
    mystring="<ol>" + mystring + "</ol>"
    return render(request, 'show_the_model_data_bulk_stored.html', {'allofit':  mystring})




