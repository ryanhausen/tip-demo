import os

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

def search(client:ElsClient, query:str):
    doc_search = ElsSearch(query, 'scopus')
    doc_search.execute(client)
    print(doc_search.results)

def main():
    client = ElsClient(os.environ['SCOPUS_KEY'])
    search(client, 'TITLE-ABS-KEY(Eliciting Categorical Data for Optimal Aggregation)')

if __name__=="__main__":
    main()