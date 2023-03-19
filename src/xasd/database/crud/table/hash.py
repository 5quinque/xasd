import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Hash as HashModel


class Hash(Table):
    table = HashModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = HashModel.hash
