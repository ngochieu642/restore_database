import pandas as pd
import time
import sqlalchemy as db
import os

def generateDatabaseString(user="ted", password="ted",
                           port=54320, host_ip="172.18.0.1",
                           database_name="sendodb"):

    db_string = 'postgres://' + user + ':' + str(password) + \
                        '@' + str(host_ip) + ':' + str(port) + '/' + database_name
    return db_string

def create_tables(sqlString,
                  user="ted", password="ted", port=54320, host_ip="172.18.0.1", database_name="sendodb"):
    db_string = generateDatabaseString(user=user, password=password, port=port,
                                        host_ip=host_ip, database_name=database_name)
    engine = db.create_engine(db_string)

    try:
        engine = db.create_engine(db_string, echo=True)
        with engine.connect() as con:
            rs = con.execute(sqlString)
        print("Successfully create tables")
    except:
        print('Failed to create tables')
        pass

def restore_database(database_directory,
                     user="ted", password="ted", port=54320, host_ip="172.18.0.1", database_name="sendodb"):

    db_string = generateDatabaseString(user=user, password=password, port=port,
                                        host_ip=host_ip, database_name=database_name)
    engine = db.create_engine(db_string)

    user_df = pd.read_json(os.path.join(database_directory,'user_train.json'))
    product_df = pd.read_json(os.path.join(database_directory,'product.json'))
    category_df = pd.read_json(os.path.join(database_directory,'category.json'))
    cate_prod_df = pd.read_json(os.path.join(database_directory,'cate_prod.json'))

    startTime = time.time()
    user_df.to_sql('users', con=engine, if_exists='append',index=False)
    category_df.to_sql('category', con=engine, if_exists='append',index=False)
    product_df.to_sql('products', con=engine, if_exists='append',index=False)
    cate_prod_df.to_sql('cate_product',con=engine, if_exists='append', index=False)
    print("Operating Time: ", time.time() - startTime, " seconds")
