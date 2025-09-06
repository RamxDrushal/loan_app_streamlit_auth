import os
import mysql.connector
import streamlit as st

def _cfg_from_secrets_or_env():
    if "db" in st.secrets:
        cfg = st.secrets["db"]
        return {
            "host": cfg.get("host", "localhost"),
            "port": int(cfg.get("port", 3306)),
            "user": cfg.get("user", "root"),
            "password": cfg.get("password", "RootPassword1"),
            "database": cfg.get("database", "loan_app"),
        }
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "RootPassword1"),
        "database": os.getenv("DB_NAME", "loan_app"),
    }

def get_connection():
    cfg = _cfg_from_secrets_or_env()
    try:
        conn = mysql.connector.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            autocommit=True,
            connection_timeout=10,
        )
        return conn, None
    except mysql.connector.Error as err:
        return None, err

def ensure_users_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      email VARCHAR(255) NOT NULL UNIQUE,
      password_hash VARCHAR(100) NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        return None
    except mysql.connector.Error as err:
        return err

def ensure_data_table(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS data (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      gender VARCHAR(10),
      age INT,
      marital_status VARCHAR(20),
      dependents INT,
      education VARCHAR(50),
      employment_status VARCHAR(50),
      residential_status VARCHAR(50),
      annual_income DECIMAL(15,2),
      monthly_income DECIMAL(15,2),
      credit_score INT,
      existing_loans INT,
      total_existing_loan_amount DECIMAL(15,2),
      loan_amount_requested DECIMAL(15,2),
      loan_term INT,
      loan_purpose VARCHAR(50),
      bank_account_history INT,
      eligibility VARCHAR(20),
      confidence FLOAT,
      suggested_amount DECIMAL(15,2),
      final_eligibility VARCHAR(20),
      final_confidence FLOAT,
      approved_amount DECIMAL(15,2),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        return None
    except mysql.connector.Error as err:
        return err
