from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types
import pickle

"""
Works well on first part of this lecture (test_text.txt)
https://www.youtube.com/watch?v=XbIfFY_fJ_s

"""

def process_file():
    client = language.LanguageServiceClient()

    file = open("test_text.txt", "r")
    text = file.read()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_entities(
        document=document,
        encoding_type='UTF32',
    )
    wikipedia_entities = {}

    for entity in response.entities:
        if 'wikipedia_url' in entity.metadata:
            print('=' * 20)
            print('         name: {0}'.format(entity.name))
            print('         type: {0}'.format(entity.type))
            print('     metadata: {0}'.format(entity.metadata))
            print('     salience: {0}'.format(entity.salience))
            wikipedia_entities[entity.name] = entity.metadata['wikipedia_url']

    pickle.dump(wikipedia_entities, open("test_text.p", "wb"))
    print("All done!")


def load_pkl():
    wikipedia_entities = pickle.load(open("test_text.p", "rb"))
    print(wikipedia_entities)


if __name__ == "__main__":
    # process_file()
    load_pkl()
