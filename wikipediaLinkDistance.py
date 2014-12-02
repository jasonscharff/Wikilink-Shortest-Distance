import urllib
import Queue
STARTER = "/wiki/"
PREFIX = "http://en.wikipedia.org"
def auxParseLinks(url):
    stream = urllib.urlopen(url)
    items = []
    for line in stream :
        indexOfTagStart = line.find("<a href")
        while indexOfTagStart != -1 :
            indexOfEnd = line.find("</a>")
            string = line[indexOfTagStart : indexOfEnd + 4]
            line = line[indexOfEnd + 4 :]
            string = getURLFromTag(string)
            if isProperLink(string, url):
                string = addPrefix(string)
                if string not in items:
                    items.append(string)
            indexOfTagStart = line.find("<a href")

    return items


def getURLFromTag(string):
    indexOfStart = string.find("=\"")
    temp = string[indexOfStart + 2:]
    indexOfEnd = temp.find("\"")
    url = temp[:indexOfEnd]
    return url

def isProperLink(string, givenLink):
    if string.find(STARTER) == 0 and string.find(".") == -1 and string.find(":") == -1 and string.find("disambiguation") == -1 and \
                    string.find("Main_Page") == - 1 and PREFIX + string != givenLink:
        return True
    else:
        return False


def addPrefix (string):
    return PREFIX + string


def parseLinks(name):
    url = convertToURL(name)
    return auxParseLinks(url)

def contains(string, array):
    if string in array:
        return True
    else:
        return False

def convertToURL(name):
    newURL = "http://en.wikipedia.org/wiki/"
    for i in range (0, len(name)):
        if name[i] == " ":
            newURL += "_"
        else:
            newURL += name[i]
    return newURL

class node:
    def __init__(self, Parent, Contents):
        self.parent = Parent
        self.contents = Contents

def buildPath(node):
    listOfLocations = []
    while node.parent != None:
        listOfLocations.append(node.contents)
        node = node.parent
    listOfLocations.append(node.contents)
    return listOfLocations



def searchAndBuild(term, target):
    queuedItems = Queue.Queue()
    targetURL = convertToURL(target)
    termURL = convertToURL(term)
    root = node(None, termURL)
    array = auxParseLinks(termURL)
    for item in array:
        n = node(root, item)
        if n.contents == targetURL:
            path = buildPath(n)
            return path
        queuedItems.put(n)
    while queuedItems.empty() == False:
        item = queuedItems.get()
        array = auxParseLinks(item.contents)
        for itemLevelTwo in array:
            n = node (item, itemLevelTwo)
            if n.contents == targetURL:
                path = buildPath(n)
                return path
            queuedItems.put(n)

array = (searchAndBuild("Yiaway Yeh", "SAT"))
print(array)