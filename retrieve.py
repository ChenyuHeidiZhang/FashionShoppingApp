# An interactive script that retrieves an item from the postgresql database, based on the input.

from model import Retriever
from app import Item

import pandas as pd
import validators
import os

if __name__ == "__main__":
    items_data = Item.query.all()
    df = pd.DataFrame.from_records([item.to_dict() for item in items_data])

    print(df.head())

    print("Construsting retriever...")
    retriever = Retriever(df)
    print("Done")

    while True:
        user_input = input('Please input search query (text, or url/path to image): ')
        if os.path.exists(user_input) or validators.url(user_input):
            mode = 'img'
        else:
            mode = 'text'
        top_items = retriever.retrieve(user_input, mode)
        #print(top_items)
        print()
