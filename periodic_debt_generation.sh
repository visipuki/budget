#! /bin/bash

db_file="db.sqlite3"
if [ ! -e $db_file ]
then
  echo "db is missed"
  exit 1
fi
get_periodic_debt="select id, period, staticDebt_id, last_generation_date from debt_periodicdebt;"
for periodic_debt in $(sqlite3 $db_file "$get_periodic_debt")
do
  periodic_id=${periodic_debt:0:1}
  period=${periodic_debt:2:1}
  static_id=${periodic_debt:4:1}
  last_generated=$(date -d${periodic_debt:6} +%F)
  if [ $period=="m" ]
  then
    first_day_in_sec=$(date -d$(date +%Y-%m-01) +%s)
    last_generated_in_sec=$(date -d"$last_generated" +%s)
    if [ $last_generated_in_sec -lt $first_day_in_sec ]
    then
      echo "$(date +%F\ %T)| periodic debt record's found | $periodic_debt"
      insert_debt="insert into debt_debt values (null,$static_id,$periodic_id,'автоматически сгенерировано на $(date +%b)','$(date +%F\ %T)');"
      update_periodic_date="update debt_periodicdebt set last_generation_date='$(date +%F)' where id=$periodic_id;"
      echo $insert_debt
      sqlite3 $db_file "$insert_debt" && echo "new debt is created"
      echo $update_periodic_date
      sqlite3 $db_file "$update_periodic_date" && echo "generation date is updated"
    fi
  fi
done
