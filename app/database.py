import sqlite3

def init_db():
    # Using file-based SQLite database for local setup
    conn = sqlite3.connect('metadata.db')  
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ImageMetadata (
            id INTEGER PRIMARY KEY,
            original_filename TEXT,
            original_size NUMERIC,
            processed_filename TEXT,
            processed_size NUMERIC,
            upload_date DATETIME,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_metadata(original_filename, original_size, processed_filename, processed_size, upload_date, description):
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO ImageMetadata (original_filename, original_size, processed_filename, processed_size, upload_date, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (original_filename, original_size, processed_filename, processed_size, upload_date, description))
    conn.commit()
    conn.close()

def get_metadata():
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ImageMetadata')
    metadata = c.fetchall()
    conn.close()
    return metadata
