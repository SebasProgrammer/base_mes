import datetime as dt
from pytz import timezone

def get_current_quarter_earliest_date() -> dt.date:
  current_Lima_date = dt.datetime.now(timezone('America/Lima'))
  return current_Lima_date.replace(
    month = 1 + 3*((current_Lima_date.month - 1)//3), 
    day = 1
  ).date()


def get_quarter_period(current_quarter_earliest_date: dt.date) -> str:
  if current_quarter_earliest_date.month == 1:
    return ''.join([
      str(current_quarter_earliest_date.year - 1),
      '-4T'
    ])
  
  return ''.join([
    str(current_quarter_earliest_date.year),
    '-',
    str(current_quarter_earliest_date.month // 3),
    'T'
  ])

if __name__ == '__main__':

    current_date = get_current_quarter_earliest_date()
    current_quarter = get_quarter_period(current_date)

    print(current_quarter)
