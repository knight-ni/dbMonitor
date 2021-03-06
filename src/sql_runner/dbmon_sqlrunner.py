from db_connector import dbmon_connector
import pandas as pd


class SQL_Runner:
    def __init__(self, dbconn):
        self.dbpool = dbconn

    def runsql(self, sqlstr):
        myconn = self.dbpool.getconn()
        df = pd.read_sql(sqlstr, con=myconn, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
        data = {col: df[col].tolist() for col in df.columns}
        return data

    def conn_is_alive(self):
        try:
            self.runsql('select 1 from sysmaster:sysdual')
            return True
        except Exception:
            return False

    def conn_exit(self):
        self.dbpool.closeconn()


if __name__ == "__main__":
    runner = SQL_Runner('jsvfpredbs')
    res = runner.runsql('select first 10 (rownumber() over (order by us_nlocks desc))::varchar(20) rank,current::varchar(32) curtime,tx_id::varchar(20) tx_id, c.sid::varchar(20) sid, trim(username) username, pid::varchar(20) pid, trim(tty) tty, trim(feprogram) feprogram, trim(sqs_statement) sqs_statement, sqs_sqlerror::varchar(20) sqs_sqlerror, sqs_isamerror::varchar(20) sqs_isamerror, tx_logbeg::varchar(20) tx_logbeg, tx_loguniq::varchar(20) tx_logcur, g.lognum::varchar(20) max_log_num, max_sortdiskspace::varchar(20) max_sortdiskspace, us_nlocks::varchar(20) us_nlocks, us_isread::varchar(20) us_isread, us_iswrite::varchar(20) us_iswrite, us_isrwrite::varchar(20) us_isrwrite, us_isdelete::varchar(20) us_isdelete from sysmaster:systrans a, sysmaster:sysuserthreads b, sysmaster:syssessions c, sysmaster:syssqlstat d, sysmaster:sysconfig e, sysmaster:syssesprof f, (select count(*) lognum from sysmaster:syslogs) g where a.tx_addr = b.us_txp and b.us_uid = c.uid and b.us_sid = c.sid and c.sid = d.sqs_sessionid and c.sid = f.sid and e.cf_name = \'LTXHWM\' and username<>\'dbmon\'')
    print (res)
