from db import DBConnection, DBOperator

with DBConnection('local.db') as db_conn:
    db_op = DBOperator(db_conn)
    ret = db_op.insert_job('Product Owner - MLOps and DataOps', 'Sep 2022', 'Present', 'Lockheed Martin - Missiles and Fire Control')
    print(ret)