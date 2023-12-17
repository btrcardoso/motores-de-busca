from cran import Cran
from search import Search
from pprint import pprint
import timeit


''' ------------------------------------------------------ Cran ------------------------------------------------------ '''

''' cria o objeto Cran para os x primeiros documentos do arquivo '''
cranObj = Cran(400)
documentsCran = cranObj.list


''' ------------------------------------------------- ElasticSearch ------------------------------------------------- '''

''' cria objeto de busca no ElasticSearch '''
es = Search()

''' etapa de indexação dos documentos. Executar somente uma vez. '''
# response = es.reindexCran(documentsCran)
# print(response)

''' busca as queries do arquivo de queries '''
queriesCran = cranObj.getQueries(10) # (365)

''' array para armazenar informações das consultas no ElasticSearch. Devem seguir o padrão: {numQuery, precision, recall, k, searchTime} '''
esResults = []

for queryObj in queriesCran:

    query = queryObj["query"]
    numQuery = queryObj["numQuery"]
    from__ = 0

    # print("\n\nBuscando respostas da query '("+str(numQuery)+") "+ query + "': ")

    ''' Documentos parecidos com a query, baseados no cranqrel '''
    cranQueryDocs = cranObj.getRelevantDocsToQuery(numQuery)
    # print("Documentos parecidos com a query, baseados no cranqrel: "+str(cranQueryDocs))

    ''' Setando o valor de documentos a serem trazidos '''
    # k = len(cranQueryDocs) 
    # if(k<=0):
    #     k=1
    k=49

    ''' faz a busca no elastic search '''
    beforeSearch = timeit.default_timer()
    response = es.search(query={
            'multi_match': {
                'query': query,
                'fields': ['name', 'summary', 'content'],
            }
        }, size=k, from_=from__
    )
    afterSearch = timeit.default_timer()
    searchTime = afterSearch - beforeSearch

    ''' a lista de resultados encontrados '''
    resultList = response['hits']['hits'] 

    ''' Documentos parecidos com a query, baseados no ElasticSearch '''
    esQueryDocs = []
    for result in resultList:
        source = result['_source']
        doc_num = source['doc_num']
        esQueryDocs.append(int(doc_num))
    # print("Documentos parecidos com a query, baseados no ElasticSearch: "+str(esQueryDocs))

    ''' obtém relações entre os dois conjuntos de documentos '''
    EsQueryDocsSet = set(esQueryDocs)
    cranQueryDocsSet = set(cranQueryDocs)
    inter = EsQueryDocsSet.intersection(cranQueryDocsSet)
    union = EsQueryDocsSet.union(cranQueryDocsSet)
    # print("Interseção: "+str(inter))
    
    ''' precision@k: dos k documentos recuperados x por cento são relevantes '''
    precision = ( len(inter) / k ) * 100
    # print("Precision@k: "+str(precision))

    ''' recall@k: x por cento do número total de itens relevantes do cranqrel aparecem nos primeiros k resultados do ElasticSearch. '''
    recall = ( len(inter) / len(cranQueryDocsSet) ) * 100
    # print("Recall@k: "+str(recall))

    esResults.append({"numQuery": numQuery, "precision": precision, "recall": recall, "k":k, "searchTime":searchTime})

pprint(esResults)


'''whoosh'''

# from searchWhoosh import SearchWhoosh

# searchWhooshObj = SearchWhoosh()