from app_src.common.common import db


def getUserRole(user_id):
    sql = "select distinct authority_name from user a,user_role b,authority c,role_authority d " \
          "where a.user_id=b.user_id and b.role_id=d.role_id and d.authority_id=c.authority_id and b.user_id=:v1"
    res = db.execute(sql, [user_id]).fetchall()
    return [i[0] for i in res] if res else 'others'





