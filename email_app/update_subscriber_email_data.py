from apscheduler.schedulers.background import BackgroundScheduler
from email_app.views.sending_views import fetch_subscriber_data_by_api_wwe360


def start():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(fetch_subscriber_data_by_api_wwe360, "interval", seconds=10,
                      id="fetch_email_data_001",
                      replace_existing=True)
    scheduler.start()
    print('scheduler started!')
