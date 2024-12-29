from dart_fss_hong import dart_fss as dart
import datetime 
import math

MAX_FETCH_MONTH = 3

# Open DART API KEY 설정
api_key='fb9d80201d79c9b4981a8b8d9e3494bc3e18fa75'
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
# corp_list = dart.get_corp_list()

# 삼성전자 검색
# samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]

# 2012년부터 연간 연결재무제표 불러오기
# fs = samsung.extract_fs(bgn_de='20120101')

# 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
# fs.save()

def get_next_month_first_day(date):
    if date.month == 12:
        return datetime.datetime(date.year + 1, 1, 1).month
    return date.month + 1

def get_date_last_day(date):
    if date.month == 12:
        return datetime.datetime(date.year, date.month, 31)
    return datetime.datetime(date.year, date.month + 1, 1) - datetime.timedelta(days=1)

def get_date_prev_months(from_date, prev_months, is_last_day=False):
    year = from_date.year
    month = from_date.month
    for i in range(prev_months):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return get_date_last_day(datetime.datetime(year, month, 1)) if is_last_day else datetime.datetime(year, month, 1)

def get_last_day_of_month(year, month):
    if month == 12:
        return datetime.datetime(year, month, 31)
    return datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

def get_report_list_from_current_to_prev_month(prev_month):
    api_call_count = math.ceil(prev_month / MAX_FETCH_MONTH)
    end_date_will_fetch = datetime.datetime.now()
    bgn_date_will_fetch = get_date_prev_months(end_date_will_fetch, MAX_FETCH_MONTH - 1)

    will_fetch_count = prev_month

    result_report_list = []

    for _ in range(api_call_count):
        print("bgn_date_will_fetch: " + bgn_date_will_fetch.strftime("%Y%m%d"))
        print("end_date_will_fetch: " + end_date_will_fetch.strftime("%Y%m%d"))
        current_page = 1
        total_page = 9999

        while current_page <= total_page:
            search_all = dart.filings.search(bgn_de=bgn_date_will_fetch.strftime("%Y%m%d"), end_de=end_date_will_fetch.strftime("%Y%m%d"), page_count=100, corp_cls="K", page_no=current_page)
            total_page = search_all.total_page
            result_report_list.extend(search_all.report_list)
            current_page += 1
            print("total page: " + str(total_page))

        will_fetch_count -= MAX_FETCH_MONTH
        bgn_date_will_fetch = get_date_prev_months(bgn_date_will_fetch, min(will_fetch_count, MAX_FETCH_MONTH))
        end_date_will_fetch = get_date_prev_months(end_date_will_fetch, MAX_FETCH_MONTH, is_last_day=True)
        
        # result_report_list.extend(search_all.report_list)
        # print(search_all.report_list)

    print(len(result_report_list))
    return result_report_list

def get_report_list_filtered_by_report_nm(report_list, report_nm):
    return [report for report in report_list if report_nm in report.report_nm]

report_list = get_report_list_from_current_to_prev_month(12)
filtered_report_list = get_report_list_filtered_by_report_nm(report_list, "유형자산")

for report in filtered_report_list:
    print(report.report_nm)
    print(report.corp_name)

# date_now = datetime.datetime.now()

# page_no = 1

# while True:
#     search_all = dart.filings.search(bgn_de="20240330", end_de="20240630", page_count=100, corp_cls="K", page_no=page_no)
#     if not search_all.report_list:
#         break
#     filtered_reports = [report for report in search_all.report_list if "유형자산" in report.report_nm]
#     for report in filtered_reports:
#         print(report.report_nm)
#         print(report.corp_name)
#     page_no += 1

# search_all = dart.filings.search(bgn_de="20240330", end_de="20240630", page_count=100, corp_cls="K", page_no=page_no)
# # print(len(search_all.report_list))
# print("total Count" + str(search_all.total_count))

# filtered_reports = [report for report in search_all.report_list if "유형자산" in report.report_nm]
# print(len(filtered_reports))
# for report in filtered_reports:
#     print(report.report_nm)
#     print(report.corp_name)

