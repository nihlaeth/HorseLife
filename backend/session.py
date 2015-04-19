from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


class SessionScope():
    def __init__(self):
        self._session = Session()

    def __enter__(self):
        return self._session

    def __exit__(self, type, value, tb):
        if type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
