from xml.dom import minidom

# Definição de funções
def indexar(arquivo):
    """
        Faz um índice invertido com os textos em que cada palavra aparece
        Retorno: 
                 - Índice invertido
                 { word     : {title: [lista de ids dos titulos em que a palavra aparece],
                               text  : [lista de ids dos textos em que a palavra aparece]}}
                 - Lista com os títulos:
                 [ id       : {id: 0, title: '', text: ''}]
    """
    dom = minidom.parse(arquivo)
    documentos = dom.getElementsByTagName('page')

    indice = {} # {word : {title: [], text: []}}    
    pages = {}

    # Procura em cada documento
    for doc in documentos:
        id = doc.getElementsByTagName('id')[0].childNodes[0].data
        title = doc.getElementsByTagName('title')[0].childNodes[0].data
        text = doc.getElementsByTagName('text')[0].childNodes[0].data
        # Pega primeiro as palavras do titulo
        for word in title.lower().split():
            # Se a palavra tiver menos que 4 caracteres não será encontrada
            if len(word) >= 4:
                # Verifica se essa palavra já está no índice
                if word in indice:
                    # Se sim, adiciona no título
                    indice[word]['title'].append(id)
                else:
                    # Caso não, cria uma nova palavra no índice
                    indice[word] = {'title': [id], 'text': []}
        # Pega as palavras do texto
        for word in text.lower().split():
            if len(word) >= 4:
                if word in indice:
                    indice[word]['text'].append(id)
                else:
                    indice[word] = {'title': [], 'text': [id]}
        # Adiciona na lista de páginas
        pages[id] = {'id': id, 'title': title, 'text': text}
    return indice, pages

def get_relevancia(item):
    return item[1]['relevancia']

def search(title, index, pages):
    """
        Procura palavra title no índice e retorna uma lista com cada texto que ela aparece(e sua relevância)
        Retorno:
        {id, {'relevancia' : X, page: { 'id'   : id, 'title': title, 'text' : text}, 'info': {'title': Y, 'text': Z}}}
        - 'relevancia'  : A importância do texto para a pesquisa
        - 'page'        : Página com o id, titulo e texto
        - 'info'        : Quantas vezes essa palavra foi encontrada no titulo e no texto
        Se info['title'] != 0, a pontuação = info['text'] * 2
    """
    ret = {}

    print('pesquisando por', title )

    # Verifica primeiro se temos essa palavra no índice
    if title.lower() in index:
        # Adiciona na resposta
        # Primeiro os títulos
        for id in index[title.lower()]['title']:
            if id in ret:
                # Já existe - Adiciona na quantidade de titulos
                ret[id]['info']['title']+=1
            else:
                # Não existe - Cria um novo
                ret[id] = {'relevancia': 0, 'page': pages[id], 'info': {'title': 1, 'text': 0}}
        
        # Agora os textos
        for id in index[title.lower()]['text']:
            if id in ret:
                # Já existe
                ret[id]['info']['text']+=1
            else:
                # Não existe
                ret[id] = {'relevancia': 0, 'page': pages[id], 'info': {'title': 0, 'text': 1}}
        
        # Calcula a relevância dos encontrados
        for encontrado in ret:
            ret[encontrado]['relevancia'] = ret[encontrado]['info']['text']
            if (ret[encontrado]['info']['title']):
                ret[encontrado]['relevancia']*=2

    # Verifica se a última letra da palavra é S e ignora ela
    if title[len(title) - 1] == 's':
        title = title[:-1]
        ret.update(search(title, index, pages))

    # Ordena o dict antes de retornar
    ret = dict(sorted(ret.items(), key=get_relevancia, reverse=True))
    
    return ret

if __name__ == "__main__":
    indice, pages = indexar("verbetesWikipedia.xml")
    resultado = search('power', indice, pages)
    
    print("rel\t|id\t|info\t\t\t\t|title")
    act = 0
    for texto in resultado: 
        #  if (act < 10):
            print(resultado[texto]['relevancia'], "\t", texto, "\t",  resultado[texto]['info'], "\t", resultado[texto]['page']['title'] )
            # act+=1
