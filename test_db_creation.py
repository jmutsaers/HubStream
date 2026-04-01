import sqlite3

# Create in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create tables
print("Creating user_ideas table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        used_in_run INTEGER
    )
""")

print("Creating web_ideas table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS web_ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        summary TEXT,
        source_url TEXT UNIQUE,
        source TEXT,
        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        used_in_run INTEGER
    )
""")

conn.commit()
print("Committed")

# Check tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"\nTables created:")
for table in tables:
    print(f"  - {table[0]}")

if ('user_ideas',) in tables and ('web_ideas',) in tables:
    print("\n✅ Both tables created successfully")
else:
    print("\n❌ Missing tables")

conn.close()
