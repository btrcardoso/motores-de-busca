from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import *

class SearchWhoosh:
    def __init__(self):
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT) # define o schema (estrutura de dados) que guardaremos o arquivo
        self.ix = create_in("indexdir", schema)
        
        documents = [
            {
                "title": u"First document",
                "path": u"/a",
                "content": u"This is the first document we've added happiness!"
            },
            {
                "title": u"Second document",
                "path": u"/b",
                "content": u"The second one is even more interesting!"
            }
        ]

        self.addDocuments(documents)

        # acho que ele nao busca stop-words
        self.search("which document is more interesting")

        # with self.ix.searcher() as searcher:
        #     myquery = And([Term("content", u"even"), Term("content", "one")])
        #     results = searcher.search(myquery)
        #     print(results[0])
    
    def search(self, user_query):
        user_query = user_query.replace(" ", " OR ")
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(user_query)
            results = searcher.search(query, terms=True)
            if(results):
                for result in results:
                    print(result)

    def addDocuments(self, documents):
        writer = self.ix.writer()
        for document in documents:
            writer.add_document(title=document["title"], path=document["path"], content=document["content"])
        writer.commit()
    
    def searchPlugin(self, text):
        parser = qparser.QueryParser("fieldname", self.ix.schema.schema)
        parser.remove_plugin_class(qparser.PhrasePlugin)
        parser.add_plugin(qparser.SequencePlugin())


    


