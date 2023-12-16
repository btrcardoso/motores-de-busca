import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

'''
um documento é representado por por um dicionario de campos chave/valor
'''

class Search:
    def __init__(self):
        self.es = Elasticsearch(cloud_id=os.environ['ELASTIC_CLOUD_ID'],
                                api_key=os.environ['ELASTIC_API_KEY'])
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    def create_index(self):
        self.es.indices.delete(index='my_documents', ignore_unavailable=True) # deleta um indice de nome my_documents
        self.es.indices.create(index='my_documents') # cria um indice de nome my_documents

    def insert_document(self, document):
        return self.es.index(index='my_documents', body=document) #inserir um documneto em um indice e retorna resposta do elastic search

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'my_documents'}})
            operations.append(document)
        return self.es.bulk(operations=operations) #insere vários documentos em uma única chamada de api

    # reinicia os index
    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        print(type(documents))
        return self.insert_documents(documents)
    
     # reinicia os index para uma lista de documentos qualquer
    def reindexCran(self, documents):
        self.create_index()
        print(type(documents))
        return self.insert_documents(documents)

    def search(self, **query_args):
        return self.es.search(index="my_documents", **query_args)

    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)
