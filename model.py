import encoder

from sentence_transformers import util
import faiss
import os
import numpy as np
import pandas as pd


class Retriever():
    def __init__(self, df):
        emb_size_text = 768
        emb_size_img = 512
        self.df = df
        self.text_embs = np.array(self.df['text_repr'].tolist(), dtype=np.float32)
        self.img_embs = np.array(self.df['img_repr'].tolist(), dtype=np.float32)


    def search(self, embds, q_embedding, top_k_hits=5):
        '''
        index: the faiss index used for the search
        q_embedding: embedding of the query
        top_k_hits: number of hits to output
        '''
        q_embedding = np.expand_dims(q_embedding, axis=0)

        hits = util.semantic_search(q_embedding, embds, top_k=top_k_hits)[0]  # default scoring with cosine similarity
        top_items = []
        for hit in hits[0:top_k_hits]:
            id_num = self.df.index[hit['corpus_id']]
            print("\t{:.3f}\t{}".format(hit['score'], id_num))
            item = self.df.iloc[hit['corpus_id']]
            print(item['description'], item['url'])
            d = {'_id': hit['corpus_id'], 'description': item['description'], 'url': item['url']}
            top_items.append(d)

        return top_items


    def retrieve(self, input, mode):
        ''' Retrieve items and return their urls using a vector model.
        '''
        if mode == 'img':
            if os.path.exists(input):
                emb = encoder.encode_local_img(input)
            else:
                emb = encoder.encode_img(input)
            top_items = self.search(self.img_embs, emb)
        else: 
            emb = encoder.encode_text(input)
            top_items = self.search(self.text_embs, emb)

        return top_items

