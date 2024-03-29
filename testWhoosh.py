from searchWhoosh import SearchWhoosh
from cran import Cran
from pprint import pprint
import timeit


''' ------------------------------------------------------ Cran ------------------------------------------------------ '''

''' cria o objeto Cran para os x primeiros documentos do arquivo '''
cranObj = Cran(400)
documentsCran = cranObj.list

''' ------------------------------------------------------ Whoosh ------------------------------------------------------ '''

searchWhooshObj = SearchWhoosh()

''' indexação de documentos, execute só uma vez '''
searchWhooshObj.addDocuments(documentsCran)

result = searchWhooshObj.search("aeroelastic models of heated high speed aircraft")
print(result)
