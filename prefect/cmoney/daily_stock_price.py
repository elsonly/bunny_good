from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import xlwings as xw
import pandas as pd


@task(retries=3, retry_delay_seconds=3)
def update_workbook(base_date: str):
    logger = get_run_logger()
    wb_path = f"D:\\repo\\bunny_good_v1\\prefect\\cmoney\\docs\\{__file__}.xlsm"
    logger.info(wb_path)
    wb = xw.Book(wb_path)
    sh = wb.sheets(0)
    sh.range('A2:A2').value = f"基準日:{base_date}"
    logger.info("update workbook...")
    wb.macro("工作表1.CM_Renew")()
    wb.save()
    wb.close()

@flow(retries=3, task_runner=SequentialTaskRunner())
def daily_stock_price_history():
    today = pd.Timestamp.today()
    begin_date = pd.to_datetime("200")
    while True:
        update_workbook()

@flow(retries=3, task_runner=SequentialTaskRunner())
def daily_stock_price():
    update_workbook()


if __name__ == '__main__':
    daily_stock_price()