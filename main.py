# Arquivo para executar preenchimento do banco do elastic search com os dados

from cran import Cran
from search import Search
from pprint import pprint

'''ElasticSearch'''

# Preenchendo com os dados do cran

# cria o objeto Cran para os x primeiros documentos do arquivo
cranObj = Cran(400)
documentsCran = cranObj.list

# cria objeto de busca no ElasticSearch
es = Search()

# etapa de indexação dos documentos. Executar somente uma vez.
# response = es.reindexCran(documentsCran)
# print(response)

# busca as queries do arquivo de queries
queriesCran = cranObj.getQueries(1) # (365)

for queryObj in queriesCran:

    query = queryObj["query"]
    numQuery = queryObj["numQuery"]
    from__ = 0

    print("\n\nBuscando respostas da query '"+ query + "': ")

    # Documentos parecidos com a query, baseados no cranqrel
    print("Documentos parecidos com a query, baseados no cranqrel: ")
    cranQueryDocs = cranObj.getRelevantDocsToQuery(numQuery)
    print(cranQueryDocs)

    # Setando o valor de documentos a serem trazidos
    k = 10
    if(len(cranQueryDocs) < k):
        k = len(cranQueryDocs)

    # faz a busca no elastic search
    response = es.search(query={
            'multi_match': {
                'query': query,
                'fields': ['name', 'summary', 'content'],
            }
        }, size=k, from_=from__
    )

    # a lista de resultados encontrados
    resultList = response['hits']['hits'] 

    # Documentos parecidos com a query, baseados no ElasticSearch
    print("Documentos parecidos com a query, baseados no ElasticSearch: ")
    esQueryDocs = []
    for result in resultList:
        source = result['_source']
        doc_num = source['doc_num']
        esQueryDocs.append(int(doc_num))
    print(esQueryDocs)

    # obtém relações entre os dois conjuntos de documentos 
    EsQueryDocsSet = set(esQueryDocs)
    cranQueryDocsSet = set(cranQueryDocs)
    inter = EsQueryDocsSet.intersection(cranQueryDocsSet)
    union = EsQueryDocsSet.union(cranQueryDocsSet)
    print("Interseção: ")
    print(inter)
    
    # precision@k: dos k documentos recuperados x por cento são relevantes
    precision = ( len(inter) / k ) * 100
    print("Precision@k: dos k="+str(k)+" documentos recuperados, "+str(precision)+" por cento são relevantes.")

    # recall@k: x Ppor cento do número total de itens relevantes do cranqrel aparecem nos primeiros k resultados do ElasticSearch.
    recall = ( len(inter) / len(cranQueryDocsSet) ) * 100
    print("Recall@k: "+str(recall)+ " por cento do número total de itens relevantes do cranqrel aparecem nos primeiros k="+str(k)+" resultados do ElasticSearch.")



'''whoosh'''

# from searchWhoosh import SearchWhoosh

# searchWhooshObj = SearchWhoosh()