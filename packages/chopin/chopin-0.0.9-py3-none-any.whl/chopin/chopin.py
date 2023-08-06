# -*- coding: utf-8 -*-

import random
import os
import re
import asyncio
import copy
import subprocess

import requests

class Link():
    """
    - Link.url
    - Link.ID
    - Link.artists
    - Link.download(path=None)
    - Link.delete()
    """
    def __init__(self,url,ID,artists):
        self.url = url
        self.ID = ID
        self.artists = artists.split(",")
        self._path = "/tmp/{}.mp3".format(ID)

    def __str__(self):
        s = "{"
        s += "'url': {}".format(self.url)
        s += ", 'ID': {}".format(self.ID)
        s += ", 'artists': {}".format(self.artists)
        s += "}"
        return s

    def download(self, path=None) -> str:
        if path and ".mp3" in path:
            self._path = path
        elif path and not ".mp3" in path:
            self._path = path + ".mp3"

        cmd = "youtube-dl -o " + self._path.replace("mp3","%(ext)s") + " -x -f bestaudio --audio-format mp3 --audio-quality 0 " + self.url
        subprocess.check_call(cmd.split())

        return self._path

    def delete(self):
        if os.path.exists(self._path):
            os.remove(self._path)

class Composition():
    """
    - Composition.title
    - Composition.Opus
    - Composition.No
    - Composition.links -> [Link()]
    - Composition.wikiLink
    """
    def __init__(self,title,Op,No,wikiLink):
        self.title = title
        self.Opus = None if Op == "ㅤ" else Op
        self.No = None if No == "ㅤ" else No
        self.links: list(Link) = []
        self.wikiLink = wikiLink

    def __str__(self):
        s = "{} ".format(self.title)
        if self.Opus:
            s += "Op.{} ".format(self.Opus)
        if self.No:
            s += "No.{}".format(self.No)
        return s

    def _appendLink(self,url,ID,artists):
        link = Link(url,ID,artists)
        self.links.append(link)

class chopin():
    def __init__(self, parallel=False, semaphore=5, output=True):
        self.compositionList = []
        while not self.compositionList:
            init = Init(output)
            if parallel:
                self.compositionList = init.mainPara(semaphore)
            else:
                self.compositionList = init.mainNotPara()
        self.genreList = [
            "Ballade",
            "Bolero",
            "Etude",
            "Fantasie",
            "Impromptu",
            "Mazurka",
            "Nocturne",
            "Concerto",
            "Sonata",
            "Scherzo",
            "Polonaise",
            "Prelude",
            "Rondo",
            "Variations",
            "Waltz",
        ]

    def _list_in_list(self,l1:list,l2:list) -> bool:
        for elm in l1:
            if not elm in l2:
                return False
        return True

    def genre(self, gen=None) -> list:
        if not gen in self.genreList:
            gen = "Others"

        outputList = []

        if gen != "Others":
            for compo in self.compositionList:
                if gen in compo.title:
                    outputList.append(copy.deepcopy(compo))
            return outputList
        else:
            for compo in self.compositionList:
                if not self._list_in_list(self.genreList, compo.title):
                    outputList.append(copy.deepcopy(compo))
            return outputList

    def get(self) -> Composition:
        outputCompo = None
        while not outputCompo:
            compo = random.choice(self.compositionList)
            if compo.links != []:
                outputCompo = copy.deepcopy(compo)
                outputCompo.links = [random.choice(compo.links)]

        return outputCompo

    def gets(self) -> Composition:
        outputCompo = None
        while not outputCompo:
            compo = random.choice(self.compositionList)
            if compo.links != []:
                outputCompo = copy.deepcopy(compo)

        return outputCompo

class Init():
    def __init__(self, output=True):
        self._wiki = Wiki(output)

    def mainNotPara(self) -> list:
        self._wiki.mainNotPara()
        return self._wiki.compoList

    def mainPara(self,semaphore) -> list:
        self._wiki.mainPara(semaphore)
        return self._wiki.compoList

class Wiki():
    def __init__(self,output=True):
        self._url = "https://github.com/ster-phys/chopin/wiki"
        text = requests.get(self._url).text
        ptn = r'<tr>\n<td align="center"><a href="(?P<link>.*?)"><img class="emoji" title=":link:" alt=":link:" src="https://camo.githubusercontent.com/fa7d9823f78ebcc07a20dc50a4c7c90d8c48cdee5f2dcacb7cd458e420ac64e8/68747470733a2f2f6769746875622e6769746875626173736574732e636f6d2f696d616765732f69636f6e732f656d6f6a692f756e69636f64652f31663531372e706e67" height="20" width="20" align="absmiddle" data-canonical-src="https://github.githubassets.com/images/icons/emoji/unicode/1f517.png"></a></td>\n<td align="left">(?P<title>.*?)</td>\n<td align="center">(?P<Opus>.*?)</td>\n<td align="center">(?P<No>.*?)</td>\n</tr>'
        self.compoList = []
        for res in re.findall(ptn,text):
            compo = Composition(res[1],res[2],res[3],res[0])
            self.compoList.append(compo)
        self.output = output

    def req(self,i:int):
        ptn = r'<tr>\n<td align="center"><a href="(?P<link>.*?)" rel="nofollow"><img class="emoji" title=":link:" alt=":link:" src="https://camo.githubusercontent.com/fa7d9823f78ebcc07a20dc50a4c7c90d8c48cdee5f2dcacb7cd458e420ac64e8/68747470733a2f2f6769746875622e6769746875626173736574732e636f6d2f696d616765732f69636f6e732f656d6f6a692f756e69636f64652f31663531372e706e67" height="20" width="20" align="absmiddle" data-canonical-src="https://github.githubassets.com/images/icons/emoji/unicode/1f517.png"></a></td>\n<td align="center"><code>(?P<ID>.*?)/code></td>\n<td align="left">(?P<artists>.*?)</td>\n</tr>'
        if self.output:
            print("{:>3}/{} Connect to {}".format(i+1,len(self.compoList),self.compoList[i].wikiLink))
        text = requests.get(self.compoList[i].wikiLink).text
        resList = re.findall(ptn,text)
        if self.output:
            print("Found {} IDs".format(len(resList)))
        for res in resList:
            self.compoList[i]._appendLink(res[0], res[1], res[2])

    def mainNotPara(self):
        for i in range(len(self.compoList)):
            self.req(i)

    async def paraRun(self,loop:asyncio.unix_events._UnixSelectorEventLoop,semaphore:int):
        sem = asyncio.Semaphore(semaphore)

        async def runReq(i):
            async with sem:
                return await loop.run_in_executor(None, self.req, i)

        tasks = [runReq(i) for i in range(len(self.compoList))]
        return await asyncio.gather(*tasks)

    def mainPara(self,semaphore):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.paraRun(loop,semaphore))
