from apscheduler.schedulers.background import BackgroundScheduler
from email_app.views.sending_views import fetch_subscriber_data_by_api_wwe360


def start():
    print('scheduler started!')
    pass
    # scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    # scheduler.add_job(fetch_subscriber_data_by_api_wwe360, "interval", hours=24,
    #                   id="fetch_email_data_001",
    #                   replace_existing=True)
    # scheduler.start()

