# Browser pool

Can be used when an easy-to-manage pool of webdrivers is needed.
Supported Windows/Linux operating systems.
To use the pool, an installed version of the browser supported by the webdriver to be used is required.
For more information about relation between version webdriver and browser see:
[Firefox version support](https://github.com/mozilla/geckodriver/releases)
and
[Chrome version support](https://chromedriver.chromium.org/downloads)


### Environments

| Name                         | Description                               | Default/Required |
|------------------------------|-------------------------------------------|------------------|
| `BROWSER_POOL_WEBDRIVER_DIR` | Directory contains webdrivers use in test | *                |
|                              |                                           |                  |