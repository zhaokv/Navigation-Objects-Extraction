# get all link in the subtree of dom
#   input: a dom-tree(maybe dom-tree)
#   output: a link list


def getLink(dom):
    linkList = []
    try:
        tmpList = dom.find_all('a')
        if dom.name == 'a':
            tmpList.append(dom)
        linkList = [link for link in tmpList if 'href' in link.attrs]
    except:
        None
    return linkList


def get_index(dom):
    index_list = []
    try:
        index_list = dom.find_all(index=True)
        if dom.attrs.get('index'):
            index_list.append(dom)
    except:
        None
    return index_list
