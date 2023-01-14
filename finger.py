import pypyodbc
import cx_Oracle as cx
from datetime import datetime
pypyodbc.lowercase = False
"""
need to add this lines as connection string
db = cx.connect('DATABASE USERNAME', 'DATABASE PASSWORD', 'DATABASE IP:UDATABASE PORT/DATABASE NAME')
dsn_tns = cx.makedsn('DATABASE IP', UDATABASE PORT, 'DATABASE NAME')
"""
curdb = db.cursor()
conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:\standard\Att2003.mdb;")
cur = conn.cursor()
cur.execute("SELECT * FROM Checkinout");
rows = cur.fetchall()
file = open("backup.csv", "a")
for row in rows: 
    
    tip=row.get("CheckType")
    idr=row.get("Userid")
    idob = "select id_oj from tba_rad where tba_rad.id_r=:idr" 
    ioj = curdb.execute(idob, [idr])
    rows = curdb.fetchall()
    
    oj = ' '.join(rows[0])
    ulaz=row.get("CheckTime")
    file.write(idr+","+str(ulaz)+"\n")
    rad="RR"
    year = ulaz.strftime("%Y")
    month = ulaz.strftime("%m")
    day = ulaz.strftime("%d")
    if tip!='I' and tip!='O':
        time = ulaz.strftime("%H:%M:%S")
        date_time = ulaz.strftime("%m/%d/%Y, %H:%M:%S")
        file.write("\n"+idr+";"+date_time+";"+tip)

    if tip=='I':
        insert = "insert into tev_evid (r_id,ulaz,vrsta_r,idoj,dat_edit) values(:idr,:ulaz,:rad,:oj,sysdate)"
        print('i')
        curdb.execute(insert, [idr,ulaz,rad,oj])
        print(idr)
        db.commit()
    elif tip=='O':
        update = "update tev_evid set izlaz=:ulaz, broj_sati=24*60*(:ulaz-ulaz),dat_edit=sysdate where ulaz in(select max(ulaz)from tev_evid where r_id=:id) and izlaz is null and r_id=:id and( to_char(ulaz,'ddmmyyyy')=to_char(sysdate,'ddmmyyyy') or  to_char(ulaz,'yyyymmdd')=to_char(sysdate-1,'yyyymmdd'))"
        print('o')
        print(idr)
        curdb.execute(update, [ulaz,ulaz,idr])
        db.commit()


file.close()
sql=("delete FROM Checkinout")
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
curdb.close()
db.close()
