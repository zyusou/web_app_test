import json
import pymongo
from tqdm import tqdm


if __name__ == '__main__':

    client = pymongo.MongoClient("localhost", 27017)
    db = client.my_mongo
    collection = db.artist_data

    with open("../resources/artist.json", mode="r", encoding="utf-8") as artist_file:
        for line in tqdm(artist_file):
            collection.insert(json.loads(line.strip()))

        collection.create_index([("name", pymongo.ASCENDING)])
        collection.create_index([("aliases.name", pymongo.ASCENDING)])
        collection.create_index([("tags.value", pymongo.ASCENDING)])
        collection.create_index([("rating.value", pymongo.ASCENDING)])
