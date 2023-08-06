import requests

def enum(domain, filename):
    r=requests.get(f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&fl=original&collapse=urlkey")
    with open(filename, 'w') as file:
        file.writelines("%s\n" % r.text)
