import subprocess
import os
from unidecode import unidecode

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


tempFolder = './tmp/'
imageFolder = './images/'
attachmentsFolder = './att/'

folders = [tempFolder, imageFolder, attachmentsFolder]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def getGDriveFileName(file: str) -> str:
    tmpFile = tempFolder+'tmp'
    runcmd("wget "+file+" -O "+tmpFile)

    title = None
    with open(tmpFile) as infile:
        for line in infile:
            if '\'title\'' in line:
                title = line.split('\'title\': \'')[1]
                # Removing accents and ascii codes
                title = (unidecode(title.split('\', \'isItemTrashed\'')[0])).replace("\\/", "/").encode('utf-8').decode('unicode_escape', 'surrogatepass')

                # Taking out the name of the user who uploaded the file.
                last = title.split(' - ')[-1]
                title = ''.join(title.split(' - ')[:-1])+'.'+last.split('.')[-1]
                break

    os.remove(tmpFile)
    return title


def downloadFiles(files: list) -> dict :
    extras = {'drive-url':[],'image':[],'attachment':[], 'url': []}

    for file in files:
        title = getGDriveFileName(file)

        if title:
            isImage = title.lower().startswith('boletin')
            outfile = imageFolder+title if isImage else attachmentsFolder+title
    
            runcmd("wget \'https://drive.google.com/uc?export=download&id="+file.replace("https://drive.google.com/open?id=","").strip()+\
                    "\' -O \""+outfile+"\"", verbose = True)

            extras['image' if isImage else 'attachment'].append(outfile.replace(imageFolder,''))
        else:
            extras['drive-url'].append(file.strip())

    return extras
