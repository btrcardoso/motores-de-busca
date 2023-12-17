from cran import Cran
from search import Search
from searchWhoosh import SearchWhoosh
from pprint import pprint
import timeit


''' ------------------------------------------------------ Cran ------------------------------------------------------ '''

''' cria o objeto Cran para os x primeiros documentos do arquivo '''
cranObj = Cran(400)
documentsCran = cranObj.list


''' ------------------------------------------------- ElasticSearch ------------------------------------------------- '''

''' cria objeto de busca no ElasticSearch '''
es = Search()

''' indexação de documentos do ElasticSearch. Executar somente uma vez. '''
# es.reindexCran(documentsCran)

''' ------------------------------------------------------ Whoosh ------------------------------------------------------ '''

''' cria objeto do Whoosh '''
searchWhooshObj = SearchWhoosh()

''' indexação de documentos do Whoosh'''
searchWhooshObj.addDocuments(documentsCran)

''' ------------------------------------------------------ Busca ------------------------------------------------------ '''


''' busca as queries do arquivo de queries '''
queriesCran = cranObj.getQueries(10) # (365)

''' array para armazenar informações das consultas no ElasticSearch e no Whoosh. Devem seguir o padrão: {numQuery, precision, recall, k, searchTime} '''
esResults = []
wResults = []

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
    k=30

    ''' faz a busca no elastic search '''
    esBeforeSearch = timeit.default_timer()
    response = es.search(query={
            'multi_match': {
                'query': query,
                'fields': ['content'],
            }
        }, size=k, from_=from__
    )
    esAfterSearch = timeit.default_timer()
    esSearchTime = esAfterSearch - esBeforeSearch
    esResultList = response['hits']['hits'] # a lista de resultados encontrados
    esQueryDocs = []
    for result in esResultList:
        source = result['_source']
        doc_num = source['doc_num']
        esQueryDocs.append(int(doc_num))
    # print("Documentos parecidos com a query, baseados no ElasticSearch: "+str(esQueryDocs))

    ''' faz a busca no whoosh'''
    wBeforeSearch = timeit.default_timer()
    wQueryDocs = searchWhooshObj.search(query)
    wAfterSearch = timeit.default_timer()
    wSearchTime = wAfterSearch - wBeforeSearch
    # print("Documentos parecidos com a query, baseados no Whoosh: "+str(wQueryDocs))

    ''' set de documentos relevantes à query no cranqrel'''
    cranQueryDocsSet = set(cranQueryDocs)

    ''' obtém relações entre os documentos do cranqrel e os documentos encontrados pelo ElasticSearch '''
    esQueryDocsSet = set(esQueryDocs)
    esInter = esQueryDocsSet.intersection(cranQueryDocsSet)
    esPrecision = ( len(esInter) / k ) * 100                        # precision@k: dos k documentos recuperados x por cento são relevantes
    esRecall = ( len(esInter) / len(cranQueryDocsSet) ) * 100       # recall@k: x por cento do número total de itens relevantes do cranqrel aparecem nos primeiros k resultados do ElasticSearch.
    esResults.append({"numQuery": numQuery, "precision": esPrecision, "recall": esRecall, "k":k, "searchTime":esSearchTime})
    
    ''' obtém relações entre os documentos do cranqrel e os documentos encontrados pelo Whoosh '''
    wQueryDocsSet = set(wQueryDocs)
    wInter = wQueryDocsSet.intersection(cranQueryDocsSet)
    wPrecision = ( len(wInter) / k ) * 100
    wRecall = ( len(wInter) / len(cranQueryDocsSet) ) * 100
    wResults.append({"numQuery": numQuery, "precision": wPrecision, "recall": wRecall, "k":k, "searchTime":wSearchTime})


''' ------------------------------------------------------ Resultados ------------------------------------------------------ '''

print("\nResultados ElasticSearch: ")
pprint(esResults)
print("\nResultados Whoosh: ")
pprint(wResults)


