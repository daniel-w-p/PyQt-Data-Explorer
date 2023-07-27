import re


class SqlValidation:

    @staticmethod
    def is_valid_dbname(dbname: str) -> bool:
        # Allowed alphanumerical data and '_'; up to 25 chars
        pattern = r'^[\w]{1,25}$'

        if re.match(pattern, dbname):
            return True
        else:
            return False
