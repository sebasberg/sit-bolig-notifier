# sit-bolig-notifier
Sends push notification to your phone when a student apartment is available for booking.

### Info
For this to work it requires to be run 24 hours. This can be done using a cloud like AWS etc. This program uses Pushover to receive push notifications. You can read more about this [here](https://pushover.net/). Read about the [api](https://pushover.net/api) and generate your API token and user key. Fill this information into constants.py in this repo. You also need to setup [selenium](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/). In constants.py you also need to fill in the url to the apartment you want to book. This program only works for [sit](https://bolig.sit.no/) (studentsamskipnaden i trondheim).
