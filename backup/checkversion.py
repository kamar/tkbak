import re
import os
import sys
import urllib
import urllib.request

response = urllib.request.urlopen('https://testpypi.python.org/pypi/tkbak/')
html = response.read()
pat = "tkbak (\d+\.\d+\.\d+)"
m = re.compile(pat)
mobj = m.search(html.decode())
print(mobj.groups())
print(mobj.group(0))
print(mobj.group(1))

def download_me(*the_urls, block_size=8192):
    """Downloads a file from a site.
USAGE: python3 downloadme.py http://1 http://2 ...
Author: Konstas Marmatakis <marmako[at]gmail[dot]com>
License: GNU/GPL v 3.0

    """
    
    for the_url in the_urls:
        the_url = urllib.parse.unquote(the_url)
        site = urllib.request.urlopen(the_url)
        r = site.info()
        #file_name = the_url.split('/)[-1:] 
        file_size = int(r.get('Content-Length'))
        file_name = the_url.split('/')[-1:][0] 
        file_seek = 0
        sinexeia = False
        if os.path.exists(file_name):
            localfile = open(file_name, 'rb')
            content = localfile.read()
            localfile.close()
            if len(content) == file_size:
                print('Το αρχείο υπάρχει ήδη.')
                break
            else:
                sinexeia = True
##        print('Κατεβάζω το αρχείο {0}.\n'.format(os.path.abspath(localfile)))
        print("Κατεβάζω: {0}\nBytes: {1} KBytes: {2:.2f}".format(os.path.abspath(file_name),\
                file_size, int(file_size/1024)))

        try:
            if sinexeia:
                fh = open(file_name, 'wb')
                megethos_arxeiou_kt = len(content)
                fh.write(content)
            else:
                fh = open(file_name, 'wb')
                megethos_arxeiou_kt = 0

            while True:
                site.read(file_seek)
                buffer = site.read(block_size)
                if not buffer:
                    break

                megethos_arxeiou_kt += len(buffer)
                fh.write(buffer)
                prcnt = (megethos_arxeiou_kt / file_size)
                
                katastasi = "{0:>6,d}kb {1:.2%}".format(round(megethos_arxeiou_kt/1024),\
                                                        prcnt)
                katastasi = katastasi + " " + "=" * int(prcnt * 100 / 2) + ">"
                sys.stdout.write("\rΚατέβηκαν: " + katastasi)
                sys.stdout.flush()

            sys.stdout.write("\n")

        finally:
            fh.close()

           
if __name__ == '__main__':
    download_me('https://testpypi.python.org/packages/source/t/tkbak/tkbak-{0}.zip'.format(mobj.group(1)))