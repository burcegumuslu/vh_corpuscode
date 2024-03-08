domain_extensions = ['.com', '.org', '.gov', '.edu', '.net', '.mil', '.io', '.co', '.info', '.me',
                     '.int', '.be', '.de', '.tv', '.news', '.ca', '.video', '.center', '.cz', '.pro', '.in', '.bab' ]
def getDomain(URL):
    try:
        x = URL.split("www.")[1]
        y = x.split("/")[0]
    except:
        try:
            x = URL.split("://")[1]
            y = x.split("/")[0]
        except:
            try:
                y = URL.split("/")[0]
            except:
                y = URL
    for domain_extension in domain_extensions:
        try:
            v = y.split(domain_extension)
            if '.' in v[0]:
                z = v[0].split('.')[1]
                domain = z + domain_extension + v[1]
            else:
                z = v[0]
                domain = z + domain_extension + v[1]
            break
        except:
            domain = y
    return domain