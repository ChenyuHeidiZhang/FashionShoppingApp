from app import db, Item
import csv

def recover_array(emb_str):
    '''Reconstructs the embedding array from csv entry string.'''
    arr = emb_str.strip('[]').split()
    arr = [float(x) for x in arr]
    return arr

def add_items():
    filename = "items.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip header
        for row in csv_reader:
            new_item = Item(description=row[1],
                img_url=row[2],
                url=row[3],
                brand=row[4],
                price=row[5],
                color=row[6],
                text_repr=recover_array(row[7]),
                img_repr=recover_array(row[8]))
            db.session.add(new_item)
            db.session.commit()
    #items_data = Item.query.all()
    #print(items_data)


if __name__=="__main__":
    db.create_all()
    add_items()


