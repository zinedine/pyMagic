"""
Warning: on Windows, the Qt database system randomly keeps the underlying .sqlite file open, making it impossible to
delete the bloody thing - which makes unit testing hard as my tests DO delete the .sqlite file each time around.

The code below IS NOT USED in this project.

The code here wraps up the QSqlQuery and QSqlDatabase objects - providing much more pythonic/easy access to everyday
tasks, e.g. to run a query with bound params, without this, you do:
    query = QSqlQuery(self.db)
    if query.prepare(query_string):
        count = 0
        for param in binding_list:
            query.bindValue(count, param)
            count += 1
    for result in query.next():
        # do stuff...

with this wrapper, you do this instead:
    query = wrapper.prepare("blah blah blah my SQL goes here")
    for res in query.next():
        # do stuff...
"""
from datetime import datetime
import weakref
from PyQt4.QtCore import QObject
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
import logging
logger = logging.getLogger(__name__)

class qtDatabaseConnection(object):
    @staticmethod
    def uniqueName():
        time_str = str(datetime.now())
        return time_str

    @staticmethod
    def databaseConnection(filename):
        driver = "QSQLITE"
        connectionName = filename + "--" + qtDatabaseConnection.uniqueName()

        if not driver in QSqlDatabase.drivers():
            logger.critical("ABORT, the {0} drive isn't available".format(driver))
            return None

        db = None
        if not QSqlDatabase.contains(connectionName):
            QSqlDatabase.addDatabase(driver, connectionName).setDatabaseName(filename)

        db = QSqlDatabase.database(connectionName, open=False)
        if not db.isOpen():
            db.open()

        if db.isOpen():
            logger.info("returning db connection called: {0}".format(db.connectionName()))
            return qtDatabaseWrapper(db)

        logger.critical("ABORT, failed to open the database for storage - tried to use filename: {0}".format(filename))

        return None

class qtDatabaseWrapper(QObject):
    def __init__(self, db):
        self.db = db
        #self.query_set = weakref.WeakSet()
        self.query_set = set()

    def __del__(self):
        self.db.commit()
        for q in self.query_set:
            logger.debug("cleaning up query: {0}".format(q.lastQuery()))
            q.finish()
            del q
        self.query_set = set()
        logger.debug("cleaning out db connection: {0}".format(self.db.connectionName()))
        self.db.close()
        QSqlDatabase.removeDatabase(self.db.connectionName())
        self.db = None

    def __refQuery(self, q):
        self.query_set.add(q)

    @staticmethod
    def bindparams(query, binding_list = ()):
        count = 0
        for param in binding_list:
            query.bindValue(count, param)
            count += 1

    def prepare(self, query_string):
        query = QSqlQuery(self.db)
        query.setForwardOnly(True)
        # weird; QSqlQuery instances don't appear to be GC'ed by the time the DB is closed - so I capture them in a strong-ref'd
        # set and finish them up myself manually.
        self.__refQuery(query)
        if query.prepare(query_string):
            return query
        raise SyntaxError("failed to prepare query, sql was: '{}', db error: {}".format(query_string, query.lastError().text()))

    def execute(self, sql_string, binding_list = ()):
        query = self.prepare(sql_string)
        qtDatabaseWrapper.bindparams(query, binding_list)
        if not query.exec_():
            raise RuntimeError("failed to exec() SQL string: '{}', db error: {}".format(sql_string, query.lastError().text()))
        return query

    @staticmethod
    def bind_and_exec(query, binding_list = ()):
        qtDatabaseWrapper.bindparams(query, binding_list)
        if not query.exec_():
            raise RuntimeError(
                "failed to exec(), db error: {}".format(query.lastError().text()))
        else:
            logger.debug("RUN STATEMENT {0}".format(query.executedQuery()))
    def handle(self):
        return self.db
            