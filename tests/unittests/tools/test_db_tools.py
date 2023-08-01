from tools import SqlValidation


class TestSqlValidation:
    def test_if_is_valid_dbname(self):
        assert SqlValidation.is_valid_dbname('yes') is True
        assert SqlValidation.is_valid_dbname('_a_') is True
        assert SqlValidation.is_valid_dbname('_1_') is True
        assert SqlValidation.is_valid_dbname('1_a') is True

    def test_if_not_valid_dbname(self):
        assert SqlValidation.is_valid_dbname('%^&') is False
        assert SqlValidation.is_valid_dbname('_a-') is False
        assert SqlValidation.is_valid_dbname('_1-') is False
        assert SqlValidation.is_valid_dbname('a1$') is False
