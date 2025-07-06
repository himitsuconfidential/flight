from playwright.sync_api import sync_playwright
import json
import random
def scroll_down(page, scroll_amount=100, delay=50):
    """Scrolls down the page gradually using scrollBy."""
    for _ in range(100):
        current_scroll_position = page.evaluate("window.pageYOffset")
        if current_scroll_position >= page.evaluate("document.body.scrollHeight"):
            break  # Stop scrolling if we've reached the bottom
        page.evaluate(f"window.scrollBy(0, {scroll_amount + random.randint(1,50)});")
        page.wait_for_timeout(delay + random.randint(1,50))



def run(page, querystring, first_run=False):
    # Load the Agoda page
    dcity = querystring['dcity']
    acity = querystring['acity']
    ddate = querystring['ddate']
    #e.g. https://hk.trip.com/flights/showfarefirst?dcity=hkg&acity=tyo&ddate=2024-09-01&triptype=ow&class=y&lowpricesource=searchform&quantity=1&searchboxarg=t&nonstoponly=off&locale=zh-TW&curr=HKD
    page.goto(f'https://hk.trip.com/flights/showfarefirst?dcity={dcity}&acity={acity}&ddate={ddate}&triptype=ow&class=y&lowpricesource=searchform&quantity=1&searchboxarg=t&nonstoponly=off&locale=zh-TW&curr=HKD', timeout=60000)
    # Wait for the page to load completely with a timeout of 60 seconds
    page.wait_for_timeout(10000)#wait 10 seconds for debug
    with open('extractsnapshot.html', 'w') as file: #for debug
        print(page.content())
        file.write(page.content())
    page.wait_for_load_state('networkidle', timeout=60000)  # 60 seconds in milliseconds
    #txt = "if (document.querySelectorAll('[data-code=\"DIRECT\"]')[0].querySelector('span.fui-checked') === null) document.querySelectorAll('[data-code=\"DIRECT\"]')[0].querySelector('span').click()"
    txt = """
    const el = document.querySelectorAll('[data-code="DIRECT"]')[0];
    if (el && el.querySelector('span')) {
      el.querySelector('span').click();
    }
    """
    if (first_run):
        page.wait_for_timeout(9000)
    page.evaluate(txt)
    page.wait_for_timeout(1000)
    scroll_down(page)
    # Get the HTML content of the fully rendered page
    html = page.content()

    with open(f'result.html', 'w', newline='') as file:
        file.write(str(html))
