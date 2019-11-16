# HOW TO USE

## Clone the repository

- The repository includes:\
   |-Utils \
   |-server_restore.py

## How to use

```bash
python server_restore.py --user ngochieu642 --password abc --port 54320 --host_ip 172.18.0.1 --database_name sendodb --database_directory './rename_database'
```

- This will create tables in your postgreSQL server
- It also restore the database_directory to postgreSQL server
