def lm_tryexcept(theurl):
    try:
        r = requests.get(theurl, timeout=(6.0, 6.0))  # This results in JSON
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
