from unittest.mock import patch, MagicMock
import psycopg2

def test_conexion_postgres_mock():
    with patch("psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Ejecutamos nuestro código simulado
        connection = psycopg2.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM retos;")
        
        # Assert de que todo se llamó correctamente
        mock_cursor.execute.assert_called_with("SELECT * FROM retos;")
