from workers import PostgresWorker


class TestPostgresWorker:
    @staticmethod
    def test_is_connected_default():
        assert PostgresWorker.is_connected() is False

    @staticmethod
    def test_is_ready_default():
        assert PostgresWorker.is_ready() is False
