from xml.dom import minidom
import xml.etree.ElementTree as ET

# arquivo = "./verbetesWikipedia.xml"
# tree =  ET.parse(arquivo)
# root = tree.getroot()

#Exibir tamanho da arvore
# print(tree)
# print(len(root))

# Exibir arvore completa
# filtro = "*"
# for child in root.iter(filtro):
#     print(child.text)

# pesquisar = input()

# for child in root.iter():
#      if (child.tag == "title" and pesquisar in child.text):
#         print(child.text)

def indexador(arquivo):
    dom = minidom.parse(arquivo)
    documentos = dom.getElementsByTagName('page')
    indice = {}
    pages = {}

    for doc in documentos:
        id = doc.getElementsByTagName('id')[0].childNodes[0].data
        title = doc.getElementsByTagName('title')[0].childNodes[0].data
        text = doc.getElementsByTagName('text')[0].childNodes[0].data

        for word in title.lower().split():
            if len(word) >= 4:
                if word in indice:
                    indice[word]['title'].append(id)
                else:
                    indice[word] = {'title': [id], 'text': []}
    
        for word in text.lower().split():
            if len(word) >= 4:
                if word in indice:
                    indice[word]['text'].append(id)
                else:
                    indice[word] = {'title': [], 'text': [id]}

        pages[id] = {'id': id, 'title': title, 'text': text}
    
    return indice, pages

def relevancia(item):
    return item[1]['relevancia']

def pesquisa(title, index, pages):
    ret = {}

    if title.lower() in index: 
        for id in index[title.lower()]['title']:
            if id in ret:
                ret[id]['info']['title']+=1
            else:
                ret[id] = {'relevancia': 0, 'page': pages[id], 'info': {'title': 1, 'text': 0}}

        for id in index[title.lower()]['text']:
            if id in ret:
                ret[id]['info']['text']+=1
            else:
                ret[id] = {'relevancia': 0, 'page': pages[id], 'info': {'title': 0, 'text': 1}}
            
        for encontrado in ret:
            ret[encontrado]['relevancia'] = ret[encontrado]['info']['text']
            if (ret[encontrado]['info']['title']):
                ret[encontrado]['relevancia']*=2
    
    if title[len(title) - 1] == 's':
        title = title[:-1]
        ret.update(pesquisa(title, index, pages))
    
    ret = dict(sorted(ret.items(), key=relevancia, reverse=True))
    
    return ret

if __name__ == "__main__":
    indice, pages = indexador("verbetesWikipedia.xml")
    resultado = pesquisa(input("O que você gostaria de buscar? "), indice, pages)
    
    print("rel\t|id\t|info\t\t\t\t|title")
    for texto in resultado: 
        print(resultado[texto]['relevancia'], "\t", texto, "\t",  resultado[texto]['info'], "\t", resultado[texto]['page']['title'] )
