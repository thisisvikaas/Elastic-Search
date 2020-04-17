from elasticsearch import Elasticsearch, helpers
import constants as C
import pandas
import time


def search_query(elastic_engine, elastic_index, query):

    def convert_to_df(es_result):
        print('jhere')
        rows = list()
        for element in es_result['hits']['hits']:
            result_dict = element['_source']
            result_dict['score'] = element['_score']
            rows.append(result_dict.copy())

        if not rows:
            return pandas.DataFrame()
        else:
            return pandas.DataFrame(rows)

    print('searching in ', elastic_index)
    s_time = time.time()
    es_result = elastic_engine.search(
        index=elastic_index, body=query)

    print('matched...')
    result_df = convert_to_df(es_result)
    print('time to query', time.time() - s_time)
    return result_df


if __name__ == "__main__":

    if not C.ES_CONF['user'] and not C.ES_CONF['password']:  # if your ES has authentication set up
        elastic_engine = Elasticsearch([C.ES_CONF['connection']])
    else:
        elastic_engine = Elasticsearch(
            [C.ES_CONF['connection']],
            http_auth=(C.ES_CONF['user'], C.ES_CONF['password'])
        )

    # Search query example
    result_df = search_query(elastic_engine, C.ES_CONF['index'], C.ES_SEARCH_QUERY)
#    print(result_df.head)
    result_df.to_csv('search_results.csv',index=False)
    print(result_df.count())
    print('result written to search_results.csv')
