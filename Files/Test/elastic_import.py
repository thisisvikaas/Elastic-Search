from elasticsearch import Elasticsearch, helpers
import constants as C
import pandas
import time


def init_index(elastic_engine, index_name):
    if elastic_engine.indices.exists(index=index_name):
        raise Exception("Index {} already exists".format(index_name))

    status = elastic_engine.indices.create(index=index_name, body=C.ES_CREATE_INDEX)
    if 'acknowledged' in status and status['acknowledged']:
        print("successfully created index {}".format(index_name))
    else:
        raise Exception("Error: {} index not created".format(index_name))


def csv_to_data_frame(file_path):
    content_df = pandas.read_csv(file_path, encoding ='latin1')
    content_df.fillna('', inplace=True)
    return content_df


def data_frame_to_elastic(content_df, elastic_engine, elastic_index):
    s_time = time.time()
    print('Inserting data to elasticsearch @ ', elastic_index)
    json_data = convert_df_to_bulk_json(content_df, elastic_index)
    res = helpers.bulk(elastic_engine, json_data, chunk_size=1000, request_timeout=20000)
    print("elastic insert status", res[0], "---", res[1])
    print('total time', time.time() - s_time)


def convert_df_to_bulk_json(content_df, elastic_index):
    json_data = list()
    content_keys = content_df.columns.values.tolist()
    for index, row in content_df.iterrows():
        content = {"_index": elastic_index, "_type": "_doc"}
        for key in content_keys:
            content[key] = row[key]
        content["_id"] = row["tweet_id"]
        json_data.append(content.copy())
    return json_data


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

    init_index(elastic_engine, C.ES_CONF['index'])
    content_df = csv_to_data_frame(C.CSV_DATA_FILE_PATH)
    data_frame_to_elastic(content_df, elastic_engine, C.ES_CONF['index'])

    # Search query example
    result_df = search_query(elastic_engine, C.ES_CONF['index'], C.ES_SEARCH_QUERY)
#    print(result_df.head)
    result_df.to_csv('search_results.csv')
    print('result written to search_results.csv')
