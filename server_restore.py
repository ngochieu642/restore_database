from Utils import restore_database
import argparse

createTableStr = "CREATE TABLE users(\
   user_id VARCHAR UNIQUE PRIMARY KEY,\
   username VARCHAR (50) UNIQUE,\
   password VARCHAR (50),\
   mac_address VARCHAR(50),\
   history VARCHAR[],\
   interest VARCHAR[],\
   last_activity TIMESTAMP,\
   value_count integer\
);\
CREATE TABLE category(\
   cate3_id_new VARCHAR UNIQUE PRIMARY KEY,\
   cate1_id VARCHAR NOT NULL,\
   cate1_name text NOT NULL,\
   cate2_id VARCHAR NOT NULL,\
   cate2_name text NOT NULL,\
   cate3_id VARCHAR NOT NULL,\
   cate3_name text NOT NULL\
);\
CREATE TABLE products(\
   product_id VARCHAR UNIQUE PRIMARY KEY,\
   product_name text NOT NULL,\
   uri TEXT,\
   oldprice numeric,\
   price numeric,\
   status integer,\
   value_count integer\
);\
CREATE TABLE cate_product(\
   id SERIAL PRIMARY KEY,\
   cate3_id_new VARCHAR not null references category(cate3_id_new),\
   product_id VARCHAR not null references products(product_id)\
);"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--port")
    parser.add_argument("--host_ip")
    parser.add_argument("--database_name")
    parser.add_argument("--database_directory")

    args = parser.parse_args()

    user = args.user if args.user else "ted"
    password = args.password if args.password else "ted"
    port = args.port if args.port else 54320
    host_ip = args.host_ip if args.host_ip else "172.18.0.1"
    database_name = args.database_name if args.database_name else "sendodb"
    database_directory = args.database_directory if args.database_directory else "./database/rename_database"

    print("user: ", user)
    print("password: ", password)
    print("port: ", port)
    print("host ip: ", host_ip)
    print("database name: ", database_name)
    print("Database ditectory: ", database_directory)

    restore_database.create_tables(sqlString=createTableStr, user=user,
                                   password=password, port=port, host_ip=host_ip, database_name=database_name)
    restore_database.restore_database(
        database_directory=database_directory, user=user, password=password, port=port, host_ip=host_ip, database_name=database_name)
