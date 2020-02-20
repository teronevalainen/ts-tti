import json
import time
import requests
import argparse
from bs4 import BeautifulSoup
from collections import deque
from multiprocessing import Process, Manager, Value
import multiprocessing

def shortestPath(links, Q, start, end, returnlist, p, num):
    print(p+": Looking for shortest path...")
    i = 0
    path = {}
    path[start] = [start]
    page = Q[0]
    while (num.value):
        if i != 0:              #getting links
            page = Q.popleft()
            links = get_links(page)

        for link in links:            
            if link in end:                             # if link is our destination
                returnlist.append(path[page] + [link])
                print(p+" found it!")
                num.value = False
                return(returnlist)

            if (link not in path) and (link != page):   
                path[link] = path[page] + [link]
                if i == 0:
                    Q.append(link)
                    Q.popleft()
                    i = 1
                Q.append(link)
    # no destination
    return None


def get_links(page):
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = page[:page.find('/wiki/')]
    links = list({base_url + a['href']
                  for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
    return links


def main():
    manager = multiprocessing.Manager()
    returnlist = manager.list()                         #list from start to destination
    start = "https://en.wikipedia.org/wiki/Airplane"
    end = "https://en.wikipedia.org/wiki/Electric_aircraft"
    num = Value("d", True)
    Q = deque([start])

    links = get_links(Q[0])
    a = round(len(links)/3)                         #seperate links into 3 parth that workers work seperately
    linksfirst = links[:a]
    linkssecond = links[2*a:3*a]
    linksthrid = links[3*a:]

    p1 = Process(target=shortestPath,
                 args=(linksfirst, Q, start, end, returnlist, "Worker 1", num))
    p1.start()
    p2 = Process(target=shortestPath,
                 args=(linkssecond, Q, start, end, returnlist, "Worker 2", num))
    p2.start()
    p3 = Process(target=shortestPath,
                 args=(linksthrid, Q, start, end, returnlist, "Worker 3", num))
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    z = 1
    newdic = {}
    pages = 0
    pituus = 99999
    for a in returnlist:            #for printing
        if (len(a) < pituus):
            newdic = a
            pituus = len(a)

    print("\n")
    print(f"Shortest path (pages between: {str(pituus-2)}) is:")
    for k in newdic:
        print(k)
    print("\n")
    print("The list:")
    for i in returnlist:
        print(str(i)+"\n")
        z += 1


if __name__ == '__main__':
    starttime = time.time()

    main()

    endtime = time.time()
    totaltime = endtime - starttime
    print("\nTime: "+str(round(totaltime, 2))+" secunds")
