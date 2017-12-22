from . import db

session = db.session('hotel')

def create_pure_eligible_persons():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_PERSONS" (
  "EMPLID",
  "NAME"
) AS (
  select emplid, name
  from pure_eligible_affiliates
  union
  select emplid, name
  from pure_eligible_employees
)"""
  #print(stmt)
  result = session.execute(stmt)
  session.commit()
  return result

def create_pure_eligible_affiliates():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_AFFILIATES" (
  "EMPLID",
  "NAME",
  "JOBCODE",
  "DEPTID",
  "DEPTID_DESCR",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "CAMPUS",
  "STATUS_FLG"
) AS (
  select
    emplid,
    name, -- for testing
    um_affil_relation as jobcode,
    deptid,
    deptid_descr,
    um_college,
    um_college_descr,
    um_campus as campus,
    status_flg
 from ps_dwhr_um_affiliates@dweprd.oit a
 where poi_type = '00012'
   and status = 'A'
   and status_flg = 'C'
   and (
     (
       um_affil_relation in -- jobcode criteria table
       (select jobcode from job_codes where pool = 'A')
     ) or (
       um_affil_relation in -- only affiliates in designated jobcodes AND departments
       (select jobcode from job_codes where pool = 'C')
       and deptid in (select deptid from affiliate_departments)
     )
   )
   and um_campus in (
     'TXXX',
     'DXXX'
   )
   and um_college not in (
     'TATH',
     'TAUD',
     'TAUX',
     'TBOY',
     'TCAP',
     'TCTR',
     'TFAC',
     'TOGC',
     'THSM',
     'TINS',
     'TOBR',
     'TOHR',
     'TSVC'
   )
)"""
  #print(stmt)
  result = session.execute(stmt)
  session.commit()
  return result

def create_pure_eligible_employees():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_EMPLOYEES" (
  "EMPLID",
  "NAME",
  "JOBCODE",
  "JOBCODE_DESCR",
  "EMPL_STATUS",
  "PAYGROUP",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "CAMPUS",
  "STATUS_FLG"
) AS (
  select
    j.emplid,
    j.name, -- for testing
    j.jobcode,
    j.jobcode_descr,
    j.empl_status,
    j.paygroup,
    j.um_college,
    j.um_college_descr,
    j.rrc as campus,
    j.status_flg
  from ps_dwhr_job@dweprd.oit j
    join job_codes jc
      on j.jobcode = jc.jobcode
  where empl_status in (
    'A',
    'L',
    'P',
    'W'
  )
    and j.status_flg = 'C'
    and paygroup != 'PLH'
    and rrc not in (
      'UMRXX',
      'UMCXX',
      'UMMXX'
    )
    and um_college not in (
      'TATH',
      'TAUD',
      'TAUX',
      'TBOY',
      'TCAP',
      'TCTR',
      'TFAC',
      'TOGC',
      'THSM',
      'TINS',
      'TOBR',
      'TOHR',
      'TSVC'
    )
)"""   
  #print(stmt)
  result = session.execute(stmt)
  session.commit()
  return result

def create_employee_jobs_current():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."EMPLOYEE_JOBS_CURRENT" (
  "EMPLID",
  "EMPL_RCDNO",
  "NAME",
  "POSITION_NBR",
  "JOBCODE",
  "JOBCODE_DESCR",
  "JOB_INDICATOR",
  "EMPL_STATUS",
  "PAYGROUP",
  "DEPTID",
  "DEPTID_DESCR",
  "UM_JOBCODE_GROUP",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "CAMPUS",
  "UM_ZDEPTID",
  "UM_ZDEPTID_DESCR",
  "STATUS_FLG",
  "RECORD_SOURCE",
  "JOB_ENTRY_DT",
  "POSITION_ENTRY_DT",
  "CALCULATED_START_DT"
) AS (
  select
    j.emplid,
    to_char(j.empl_rcdno) as empl_rcdno,
    j.name, -- for testing
    j.position_nbr,
    j.jobcode,
    j.jobcode_descr,
    j.job_indicator,
    j.empl_status,
    j.paygroup,
    j.deptid,
    j.deptid_descr,
    j.um_jobcode_group,
    j.um_college,
    j.um_college_descr,
    j.rrc as campus,
    j.um_zdeptid,
    j.um_zdeptid_descr,
    j.status_flg,
    'J' as record_source, -- J for ps_dwhr_job or A for ps_um_affiliates for source
    j.job_entry_dt,
    j.position_entry_dt,
    least(j.job_entry_dt, j.position_entry_dt) as calculated_start_dt
  from ps_dwhr_job@dweprd.oit j
    join job_codes jc
      on j.jobcode = jc.jobcode
  where empl_status in (
    'A',
    'L',
    'P',
    'W'
  )
    and j.status_flg = 'C'
    and paygroup != 'PLH'
    and rrc not in (
      'UMRXX',
      'UMCXX',
      'UMMXX'
    )
    and um_college not in (
      'TATH',
      'TAUD',
      'TAUX',
      'TBOY',
      'TCAP',
      'TCTR',
      'TFAC',
      'TOGC',
      'THSM',
      'TINS',
      'TOBR',
      'TOHR',
      'TSVC'
    )
)"""   
  #print(stmt)
  result = session.execute(stmt)
  session.commit()
  return result
