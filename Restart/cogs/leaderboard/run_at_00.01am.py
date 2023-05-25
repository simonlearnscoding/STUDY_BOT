import schedule
import time

def job():
    print("It's 00:01")

schedule.every().day.at("00:01").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
