import yt2mp3down.r as r
from yt2mp3down.t import tqdm

def setup(link):
    url = "https://dl1.youtubetomp3.sc/searchdl.php"
    data = {"url":link,"type":"mp3"}
    h = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0","Connection": "keep-alive","Referer": "https://ytmp3.cc/youtube-to-mp3/"}
    res = r.post(url,headers=h,data=data)
    return res.text

def addInner(string,start,end):
    inner = ''
    tempI = 0
    if (start in string) and (end in string):
        for i in range(len(string)-len(start)-1):
            if start == string[i:(i+len(start))]:
                tempI = i+len(start)
                break

        for i in range(tempI,len(string)-len(end)-1):            
            if end == string[i:(i+len(end))]:
                break
            inner = inner + string[i]
    return inner

def tableToList(string):
    string = string.replace('<tr>','')
    stringList = string.split('</tr>')
    stringListFormated = []
    for tr in range(len(stringList)-1):
        trS = stringList[tr].splitlines()
        stringListFormated.append([])
        for td in trS:
            td = td.replace('<td>','')
            td = td.replace('</td>','')
            td = td.replace('<a href=\'','')
            td = td.replace('\' class=\'btn btn-dark btn-sm\' onclick=\'ads()\'>Download</a>','')
            td = td.strip()
            if td=='':
                continue
            stringListFormated[tr].append(td)
            
    return stringListFormated

def get(ii,fname):
    chunk_size = 1024

    url = ii[2]

    re = r.get(url, stream = True)
    total_size = float((ii[1].replace(' MB','')))*1024*1024

    with open(fname, 'wb') as f:
        for data in tqdm(iterable = re.iter_content(chunk_size = chunk_size), total = total_size/chunk_size, unit = 'KB'):
            f.write(data)

   
def download(title,link,path):
    remove = '/\:*?"\'`<>|'
    new_title = ''
    for i in title:
        if not(i in remove):
            new_title +=i
        else:
            new_title +='-'
    new_title += '.mp3'
    
    import os
    p =''
    if os.path.isdir(path):
        if path[-1]!='\\':
            p = path+'\\'
        else:
            p = path
    get(link,p+new_title)
    

def mp3(link,quality=0,path=''):
    x = setup(link)
    title = addInner(x, '<div class=\'title\'>', '</div>').strip()
    inner1 = addInner(x,'<table id=\'tab_mp3\' >','</table>')
    inner2 = addInner(inner1,'<tbody>','</tbody>')

    its = tableToList(inner2)
    if its ==[]:
        try:
            raise ValueError('Provided link isn\'t valid')
            raise Exception('Provided link isn\'t valid')
        except Exception as ex:
            print('ValueError: ' + repr(ex))
            exit()
    no = 1
    print(title)
    if quality==0:
        for i in its:
            print('[',no,']',i[0],'-',i[1])
            no+=1
        st = int(input('\nSelect - '))-1
        ii = its[st]
    else:
        for i in its:
            if (str(quality)+'Kbps')==i[0]:
                ii = i

    download(title,ii,path)