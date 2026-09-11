from unittest.mock import patch

from webapp import config
from webapp.database import get_db_connection


@patch("webapp.database.mysql.connector.connect")
def test_get_db_connection_uses_configured_mysql_settings(mock_connect):
    mock_connect.return_value = object()

    connection = get_db_connection()

    assert connection is mock_connect.return_value
    mock_connect.assert_called_once_with(
        host=config.Config.MYSQL_HOST,
        port=config.Config.MYSQL_PORT,
        user=config.Config.MYSQL_USER,
        password=config.Config.MYSQL_PASSWORD,
        database=config.Config.MYSQL_DATABASE,
    )
