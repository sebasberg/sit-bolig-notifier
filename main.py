import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import constants


def notify(msg, url_attached):
    pushover_url = "https://api.pushover.net/1/messages.json" # URL used for sending push notifications via pushover, standard url from pushover website
    token = constants.API_TOKEN
    user_key = constants.USER_KEY
    title = "Sit Bolig Notifier"
    PARAMS = {"token": token, "user": user_key, "message": msg, "title": title, "url": url_attached}
    requests.post(pushover_url, PARAMS)

# Used for sending push notifications when hosting on AWS
sent_flag = 0
def notify_script_running(msg, url_attached):
    global sent_flag
    norway_hour = time.gmtime(time.time()).tm_hour + 2
    if norway_hour == 24:
        norway_hour = 0
    if norway_hour == 25:
        norway_hour = 1
    if (norway_hour == 0 or norway_hour == 6 or norway_hour == 12 or norway_hour == 18) and not sent_flag:
        notify(msg, url_attached)
        sent_flag = 1
    if (norway_hour == 1 or norway_hour == 7 or norway_hour == 13 or norway_hour == 19) and sent_flag:
        # reset sent flag one hour after sent push notification
        sent_flag = 0
    print(f"Norway Hours: {norway_hour}, Sent Flag: {sent_flag}")
    
fail_count = 0
while True:
    apartment_url = constants.APARTMENT_URL # URL for the apartment you want to book
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(apartment_url)
    time.sleep(5)
    page = driver.page_source
    driver.quit()
    html = BeautifulSoup(page, "html.parser")

    try:
        p_tag = html.find_all("p", attrs={"class": "unit__StyledAvailableStatus-sc-157sc49-10"})[0]
        available = p_tag.span.contents[0].strip().lower()
    except Exception as e:
        fail_count += 1
        if fail_count == 100:
            notify("Det har skjedd exceptions flere ganger, sjekk at programmet kjører som det skal i AWS", url)
        print(e)

    print(f"Sit: {available}")
    if available == "ledig":
        notify("Boligen er nå ledig!", url)
        break
    elif available == "ikke ledig":
        print("Boligen er ikke ledig, fortsetter søk")
    else:
        print("Det har skjedd noe feil, sender pushvarsel")
        notify("Det har skjedd en feil i python-programmet, sjekk om bolig er ledig og om programmet virker som det skal", url)
        break
    notify_script_running(f"Sit Bolig Notifier kjører fortsatt\nSit: {available}", url)
    print()
    time.sleep(30)

