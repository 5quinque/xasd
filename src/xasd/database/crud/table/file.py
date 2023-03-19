import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import File as FileModel


class File(Table):
    table = FileModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = FileModel.track
