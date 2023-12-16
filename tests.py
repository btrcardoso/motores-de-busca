import json
from search import Search
es = Search()

with open('data.json', 'rt') as f:
    documents = json.loads(f.read())
for document in documents:
    es.insert_document(document)


def test():
    document = {
        'title': 'Work From Home Policy',
        'contents': 'The purpose of this full-time work-from-home policy is...',
        'created_on': '2023-11-02',
    }
    response = es.insert_document(document) 
    print("reposta do elastic search: ")
    print(response)
    print(response['_id'])
