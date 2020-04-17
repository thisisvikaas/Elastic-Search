ES_CONF = {
    "connection": {
        "host": "localhost",
        "port": "9200"
    },
    'user': 'elastic',   # leave it blank if you dont have authentication set up
    'password': 'elastickau',
    "index": "acc_tweets"  # Name of elasticsearch index
}

CSV_DATA_FILE_PATH = "./tweet_data_query.csv"

ES_CREATE_INDEX = """{
    "mappings": {
      "properties": {
        "created_at": {
          "type": "keyword"
        },
        "embed_html": {
          "type": "text"
        },
        "favorite_count": {
          "type": "integer"
        },
        "geo": {
          "type": "keyword"
        },
        "in_reply_to_status_id": {
          "type": "long"
        },
        "is_quoted": {
          "type": "keyword"
        },
        "is_retweet": {
          "type": "keyword"
        },
        "lang": {
          "type": "keyword"
        },
        "place": {
          "type": "keyword"
        },
        "possibly_sensitive": {
          "type": "keyword"
        },
        "quoted_status_id": {
          "type": "keyword"
        },
        "retweet_count": {
          "type": "integer"
        },
        "tweet_id": {
          "type": "text"
        },
        "tweet_text": {
          "type": "text"
        },
        "user_id": {
          "type": "text"
        }
      }
    }
}"""

ES_SEARCH_QUERY = """{
    "size":10000,
    "_source": ["uploaded_date", "created_at", "user_id", "tweet_text"],
    "query": {
      "match": {
        "tweet_text": "VICTORIA Vericiguat Heart Failure"
      }
    }
}"""