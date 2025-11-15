import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="retnova_db"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM retos;")
    rows = cursor.fetchall()
    print("Total de retos:", len(rows))


except Exception as error:
    print("❌ Error al conectar con PostgreSQL:", error)

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("🔒 Conexión cerrada.")
