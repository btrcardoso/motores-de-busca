from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import *

class SearchWhoosh:
    def __init__(self):
        schema = Schema(content=TEXT, doc_num=TEXT(stored=True), name=TEXT(stored=True), summary=TEXT, created_on=TEXT, updated_at=TEXT ) # define o schema (estrutura de dados) que guardaremos o arquivo
        self.ix = create_in("indexdir", schema)
    
    def search(self, user_query):
        user_query = user_query.replace(" ", " OR ")
        docsFound = []
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(user_query)
            results = searcher.search(query, terms=True)
            if(results):
                for result in results:
                    docsFound.append(int(result['doc_num']))
            return docsFound

    def addDocuments(self, documents):
        writer = self.ix.writer()
        for document in documents:
            writer.add_document(content=document["content"], doc_num=document["doc_num"], name=document["name"], summary=document["summary"], created_on=document["created_on"], updated_at=document["updated_at"])
            # writer.add_document(title=document["title"], path=document["path"], content=document["content"])
        writer.commit()
    
    def searchPlugin(self, text):
        parser = qparser.QueryParser("fieldname", self.ix.schema.schema)
        parser.remove_plugin_class(qparser.PhrasePlugin)
        parser.add_plugin(qparser.SequencePlugin())


    


