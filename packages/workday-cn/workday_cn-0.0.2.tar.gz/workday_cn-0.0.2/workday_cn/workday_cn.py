import datetime

CF=(
('2021-01-01','元旦'),('2021-01-02','元旦'),('2021-01-03','元旦')
,('2021-02-11','春节'),('2021-02-12','春节'),('2021-02-13','春节'),('2021-02-14','春节')
,('2021-02-15','春节'),('2021-02-16','春节'),('2021-02-17','春节')
,('2021-02-07','工作日')
,('2021-02-20','工作日')
,('2021-04-03','清明节'),('2021-04-04','清明节'),('2021-04-05','清明节')
,('2021-05-01','劳动节'),('2021-05-02','劳动节'),('2021-05-03','劳动节'),('2021-05-04','劳动节')
,('2021-05-05','劳动节')
,('2021-04-25','工作日')
,('2021-05-08','工作日')
,('2021-06-12','端午节'),('2021-06-13','端午节'),('2021-06-14','端午节')
,('2021-09-19','中秋节'),('2021-09-20','中秋节'),('2021-09-21','中秋节')
,('2021-09-18','工作日')
,('2021-10-01','国庆节'),('2021-10-02','国庆节'),('2021-10-03','国庆节'),('2021-10-04','国庆节')
,('2021-10-05','国庆节'),('2021-10-06','国庆节'),('2021-10-07','国庆节')
,('2021-09-26','工作日')
,('2021-10-09','工作日')
)

def extract_CF():
    d={}
    for i in CF:
        d[i[0]]=i[1]
    return d

def is_workday(d):
    spec_date=extract_CF()
    if isinstance(d,datetime.datetime):
        date=d
    elif isinstance(d,str):
        try:
            date=datetime.datetime.strptime(d,'%Y-%m-%d')
        except Exception as e:
            raise Exception(f'{d} type is {type(d)}, only support datetime or string like %Y-%m-%d')
    else:
        raise Exception(f'{d} type is {type(d)}, only support datetime or string like %Y-%m-%d')
    week=date.weekday()
    if week>=0 and week<=4:
        # print('workday')
        if spec_date.get(datetime.datetime.strftime(date,'%Y-%m-%d')) is None:
            # print('workday.workday1')
            return True
        elif spec_date.get(datetime.datetime.strftime(date,'%Y-%m-%d'))=='工作日':
            # print('workday.workday2')
            return True
        else:
            # print('workday.restday')
            return False
    elif week in (5,6):
        # print('restday')
        if spec_date.get(datetime.datetime.strftime(date,'%Y-%m-%d')) is None:
            # print('restday.restday1')
            return False
        elif spec_date.get(datetime.datetime.strftime(date,'%Y-%m-%d'))!='工作日':
            # print('restday.restday2')
            return False
        else:
            # print('restday.workday')
            return True
    else:
        raise Exception(f'week is {week}')

def today_is_workday():
    return is_workday(datetime.datetime.now())

# is_workday('2021-05-05 12:12:12')
# is_workday('2021-05-05')==False
# is_workday('2021-05-06')==True
# is_workday('2021-05-08')==True
# is_workday(datetime.datetime.strptime('2021-05-08','%Y-%m-%d'))==True
