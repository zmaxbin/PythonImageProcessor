# -*- coding:utf-8 -*-
import MySQLdb

def MysqlPipline():
    database_host = 'localhost'
    database_username = 'root'
    database_password = '123.'
    database_dbname = 'antifraud'
    database_charset = 'utf8'

    conn = MySQLdb.connect(database_host, database_username, database_password, database_dbname, charset=database_charset)
    return conn

def CreateDatabase():
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='123.',
        charset='utf8',
        use_unicode=False
    )
    cursor = conn.cursor()
    DB_NAME = 'antifraud'
    conn.select_db(DB_NAME)

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS loss_trust_execution(id varchar(40) primary key,execution_name varchar(20),sex varchar(20),age varchar(20),id_number varchar(60),legal_representative varchar(100),executive_court varchar(100),province varchar(40),execute_number varchar(200),filing_time varchar(100),reference_number varchar(100),make_implementation_unit varchar(100),obligation varchar(100),execution_performance varchar(100),lost_letter_specific_situation varchar(200),release_time varchar(100),update_time datetime)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS loss_trust_execution_company(id varchar(40) primary key,execution_name varchar(100),id_number varchar(100),legal_representative varchar(100),executive_court varchar(100),province varchar(60),execute_number varchar(100),filing_time varchar(100),reference_number varchar(100),make_implementation_unit varchar(100),obligation varchar(100),execution_performance varchar(200),lost_letter_specific_situation varchar(200),release_time varchar(40),update_time datetime)')
