import json
import timeit
from pprint import pprint

class Cran: 
    def __init__(self, qtDocs):
        # coleção de documentos e nomes dos documentos
        self.collectionDocs = []
        self.collectionDocsNames = []

        # percorre o arquivo de documentos de consulta às perguntas. Cada line representa um documento. guarda cada documento limpo no array "collectionDocs"
        for line in self.readFile("cran-files/cran.all.1400"):
            beforeIndex = timeit.default_timer()
            self.collectionDocs.append(self.cleanTrash(line))
            self.collectionDocsNames.append(self.getDocName(self.collectionDocs[len(self.collectionDocs) - 1]))
            afterIndex = timeit.default_timer()
            indexTime = afterIndex - beforeIndex
            #print(f"Tempo de indexar: {indexTime}")

        # trasnformando documentos na estrutura formatada
        self.list = [{'content': content.split(" ")[1], 'doc_num':content.split(" ")[0], 'name': name, 'summary': content, 'created_on':'2023-12-10', 'updated_at':'2023-12-10'} for content, name in zip(self.collectionDocs[:qtDocs], self.collectionDocsNames[:qtDocs])]
        
        # pegando o conjunto de treino (pergunta-documento-relevancia do doc pra pergunta)
        self.queriesDocsRelevancy = []
        for line in self.readFileByLine("cran-files/cranqrel"):
            answer = self.queryDocRelevancyDict(line)
            if(answer):
                self.queriesDocsRelevancy.append(answer)

    # lê o arquivo e retorna um array com as strings separadas por "\n"
    def readFileByLine(self, path):
        beforeReading = timeit.default_timer()
        with open(path, "r") as file:
            f = file.read()
        afterReading = timeit.default_timer()
        readingTime = afterReading - beforeReading
        # print(f"LOG: Tempo de leitura: {readingTime}")
        return f.split("\n")[1:]

    # lê o arquivo e retorna um array com as strings separadas por ".I"
    def readFile(self, path):
        beforeReading = timeit.default_timer()
        with open(path, "r") as file:
            f = file.read()
        afterReading = timeit.default_timer()
        readingTime = afterReading - beforeReading
        # print(f"LOG: Tempo de leitura: {readingTime}")
        return f.split(".I")[1:]
    
    # dada uma string(documento), retira símbolos desnecessários e algumas stop words
    def cleanTrash(self, string):
        beforeCleaning = timeit.default_timer()
        result = string.replace("\n"," ").replace(".T","").replace(".A","").replace(".B","").replace(".W","").replace("the ", "").replace("an ", "").replace("a ", "").strip()
        afterCleaning = timeit.default_timer()
        cleaningTime = afterCleaning - beforeCleaning
        # print(f"LOG: Tempo de limpeza: {cleaningTime}")
        return result
    
    # obtém o nome do documento
    def getDocName(self, string):
        result = string.split(".")
        return result[0]
    
    def cleanQuery(self, string):
        saida = string.replace("\n", " ").replace(".W", "").replace("the ", "").replace("an ", "").replace("a ", "").strip()
        return saida
    
    # função que retorna uma lista de queries
    def getQueries(self, quantity):
        queries = []
        count = 1
        for line in self.readFile("cran-files/cran.qry"):
            if(count > quantity):
                return queries
            query = self.cleanQuery(line)[5:]
            queries.append({"numQuery": int(self.cleanQuery(line)[:5]), "query": query})
            count += 1
        return queries
    
    # retorna um array ordenado por relevancia de dictionaries {numQuery, numDoc, relevancy}
    def getQueryDocRelevancyForQuery(self, numQuery):
        queryDocRelevancyForQuery = []
        for qdr in self.queriesDocsRelevancy:
            if(qdr["numQuery"] == int(numQuery)):
                queryDocRelevancyForQuery.append(qdr)
        return sorted(queryDocRelevancyForQuery, key=lambda x: x["relevancy"])
    
    # retorna um array com os documentos que têm alguma relevância em relação a query
    def getRelevantDocsToQuery(self, numQuery):
        queryDocRelevancyForQuery = []
        for qdr in self.getQueryDocRelevancyForQuery(numQuery):
            if(qdr["numQuery"] == int(numQuery)):
                # print("docs achados para essa query: "+str(qdr))
                queryDocRelevancyForQuery.append(qdr["numDoc"])
        return queryDocRelevancyForQuery

    # transforma uma string ("1 20 3") em um dictionary {numQuery, numDoc, relevancy}
    def queryDocRelevancyDict(self, numbers_string):
        numbers = [int(num) for num in numbers_string.split() if num.isdigit()]
        if len(numbers) == 3:
            return {
                "numQuery": numbers[0],
                "numDoc": numbers[1],
                "relevancy": numbers[2]
            }
