'''
## Download VGE picutres from the official website
## Time: 11/14/14
## Author: Edison Qian
'''
from __future__ import print_function
def download(url):
    # serial downloading
    import urllib
    # import urllib2
    # import request
    import os
    import datetime
    #url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
    base,outputFile=os.path.split(url)
    if not os.path.exists('photos'):
        os.mkdir('photos')
    outputFile=os.getcwd()+'\\photos\\'+outputFile

    print("downloading with urllib")
    print(outputFile+' is downloading......')

    start_time=datetime.datetime.now()
    urllib.urlretrieve(url, outputFile)

    size=1.0*os.path.getsize(outputFile)/1024**2# Megabyte
    costtime=(datetime.datetime.now()-start_time).seconds
    print("saved: "+outputFile+\
        '\tsize: '+str(size)+'M'+\
        '\tcost: '+str(costtime)+'s')

    # print "downloading with urllib2"
    # f = urllib2.urlopen(url)
    # data = f.read()
    # with open(outputFile, "wb") as code:
    #     code.write(data)

    # print "downloading with requests"
    # r = requests.get(url)
    # with open(outputFile, "wb") as code:
    #      code.write(r.content)

def hrefs():
    urls=[]
    ids=range(1,166);
    dir='http://www.iseis.cuhk.edu.hk/img/events/20141106_conference/'
    urls.append(dir+'00a.jpg')
    urls.append(dir+'00b.jpg')
    urls.append(dir+'00c.jpg')
    
    map(lambda i:urls.append(dir+str(i)+'.jpg'),ids)
    # print(urls)
    return urls

def write(urls):
    f=open('href.txt','w')
    map(lambda path:f.writelines(path+'\n'),urls)
    f.close()

def Run():
    write(hrefs())

    import datetime
    start_time=datetime.datetime.now()
    map(download,hrefs())
    costtime=(datetime.datetime.now()-start_time).seconds
    if costtime>60**2:
        time_msg=str(1.0*costtime/60**2)+'h'
    elif costime>60:
        time_msg=str(1.0*costtime/60)+'m'
    else:
        time_msg=str(1.0*costtime)+'s'
    print('Totall cost time: '+time_msg)

if __name__=='__main__':
    Run()
