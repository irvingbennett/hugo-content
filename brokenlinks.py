import glob
import bs4
import urllib.request
import os.path

def checkLinks(links):

  brokenCount = 0
  log = open("/tmp/brokenlinks.log", "w")
  for link in links:
   message = ""
   try:
     status_code = urllib.request.urlopen(link).getcode()
     if(status_code != 200):
       message = link + " status code: "  + status_code
   except:
     message = link + " broken"

   if message:
     brokenCount += 1
     print(message)
     log.write(link + "\n")

  log.close();
  return brokenCount

def extractLinks(files):

  httpLinks = []
  for file in files:
    with open(file) as f:
      soup = bs4.BeautifulSoup(f,features="html5lib")

    links = [link['href'] for link in soup('a') if 'href' in link.attrs]

    for link in links:
      if link.startswith('http'):
        httpLinks.append(link)

  linkSet = set()
  for link in httpLinks:
    linkSet.add(link.split('?')[0])

  return linkSet

def findFiles(dirs,pattern):
  files = list();
  for dir in dirs:
   glb = dir + '/**/' + pattern
   paths = glob.glob(glb,recursive=True)
   files.extend(paths)

  return files

def checkDirs(dirs):
  clean = True
  for dir in dirs:
    if not os.path.isdir(dir):
       print("no such dir: " + dir)
       errors = False
  return clean

# entry point

dirs = []
dirs.append('public/tutorial');
dirs.append('public/post');

if not checkDirs(dirs):
   exit()

htmlFiles = findFiles(dirs,'*.html')

links = extractLinks(htmlFiles)
print("total links: " + str(len(links)))

brokenCount = checkLinks(links)
print("broken links: " + str(brokenCount))