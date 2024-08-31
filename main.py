import tocsv
import extract
import csv
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright


# Correctly structured cookies
# Domain and path information
cookie_domain = ".trip.com"  # Replace with the correct domain
cookie_path = "/"            # Replace with the correct path if necessary

# Convert concise cookies to the structured format
concise_cookies = {
"GUID": "09034166416765545937",
"GUID.sig": "gklEu2jnJ8m_t5A7VgmgZBZH4CeH_iMW1JJnpjr_FpA",
"IBU_FLIGHT_LIST_STYLE": "Separate",
"ibulanguage": "HK",
"ibulocale": "zh_hk",
"cookiePricesDisplayed": "HKD",
"_abtest_userid": "76d0a563-8cbc-48f6-a518-32b39ad5eceb",
"UBT_VID": "1723818289094.54aeiwXd3Pjy",
"_fwb": "63TTaMowVzE6ZWnvYJGFFw.1723818290201",
"_gid": "GA1.2.94253672.1723818290",
"_tt_enable_cookie": "1",
"_ttp": "h4E6XyV1FY5E3hh76zFLCzVVSwj",
"_gcl_au": "1.1.1534360854.1723818291",
"_RF1": "123.202.133.26",
"_RSG": "xYqYMa5Ki46_yMMkZfhS.A",
"_RDG": "280e6ce58ce24e229e3fe04e2ff7bea118",
"_RGUID": "612c5059-168b-48bb-af9c-ae98ee596f3f",
"_combined": "transactionId%3D8dcdcce0-9d49-45d0-a552-78f4031164c2%26pageId%3D10320667452%26initPageId%3D10320667452",
"_bfa": "1.1723818289094.54aeiwXd3Pjy.1.1723818289175.1723818302269.1.2.10320667452",
"wcs_bt": "s_33fb334966e9:1723818302",
"_uetsid": "4c0f05e05bdb11efb86895824854b67b",
"_uetvid": "4c0f38905bdb11efa836f31708a9a040",
"_ga": "GA1.1.1300492427.1723818290",
"_ga_37RNVFDP1J": "GS1.2.1723818290.1.1.1723818303.47.0.0",
"_ga_2DCSB93KS4": "GS1.2.1723818291.1.1.1723818303.48.0.0",
"_ga_X437DZ73MR": "GS1.1.1723818290.1.1.1723818306.0.0.0"
}
cookies = []
for name, value in concise_cookies.items():
    cookies.append({
        "name": name,
        "value": value,
        "domain": cookie_domain,
        "path": cookie_path,
        "expires": -1,  # session cookie
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    })

def update_change_log():
    with open(f'change_log.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([[datetime.now().strftime('%Y%m%d'),
                        querystring['dcity'], #depart city
                        querystring['acity'], #arrival vity
                        querystring['ddate'], #depart date
                        ]])

with sync_playwright() as p:
    user_agent ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    # Choose the browser you want to use (Chromium, Firefox, or WebKit)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    context = browser.new_context(user_agent=user_agent)

    # Set cookies on the page context
    page.context.add_cookies(cookies)
    today = datetime.now()
    tmr = today + timedelta(days=1)
    tmr_string = tmr.strftime("%Y-%m-%d")
    for querystring in [{"dcity":"HKG","acity":"TYO","ddate":tmr_string},
                        {"dcity":"TYO","acity":"HKG","ddate":tmr_string}]:
        first_run = True
        for dte in range(92):
            extract.run(page, querystring, first_run)
            first_run = False
            tocsv.run()
            update_change_log()
            next_day = datetime.strptime(querystring['ddate'],"%Y-%m-%d") + timedelta(days=1)
            querystring['ddate'] = next_day.strftime("%Y-%m-%d")

    # Close the browser
    browser.close()


