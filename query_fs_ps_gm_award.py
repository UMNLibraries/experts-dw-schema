# One-off to populate person-related mds tables that do not need their own special procedures.

import db
s = db.session('hotel')

import models

columns = (
  'contract_num',
  'title56',
  'descr254',
  'ref_awd_number',
  'begin_dt',
  'end_dt',
  'deptid',
  'award_status',
)

st = (
  'select awa1.emplid, ' +
  ', '.join(['awa1.' + column for column in columns]) +
  ' from fs_ps_gm_award@dweprd.oit awa1, fs_ps_gm_award@dweprd.oit awa2 where awa1.emplid = awa2.emplid and awa1.contract_num = awa2.contract_num and awa1.dttm_stamp != awa2.dttm_stamp order by awa1.emplid desc, awa1.contract_num'
)

multiples = []

result = s.execute(st)
for row in result.fetchall()[:50]:
  print(row)
