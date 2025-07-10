from bs4 import BeautifulSoup
import csv
from datetime import datetime
def starts(txt):
    return lambda x: x and x.startswith(txt)
def find(element, tag, class_start):
    tag = element.find(tag, class_=lambda x: x and x.startswith(class_start))
    return tag

def find_all(element: object, tag: str, class_start: str)->int:
    tags = element.find_all(tag, class_=lambda x: x and x.startswith(class_start))
    return tags
def run():
    # Assuming you have the HTML content in a variable called 'html_content'
    with open('result.html') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the element with the id "J_resultList"
    result_list_element = soup.find(id="J_resultList")

    elements_with_index = result_list_element.find_all(attrs={"data-index": True})
    data = []
    airline_code_table = {'大灣區航空':'GB',
                          '香港航空':'HX',
                          '香港快運航空':'UO',
                          '國泰航空':'CX',}
    for element in elements_with_index:

        print(element.text)
        airline = element.find('span', class_ = 'airline-base')
        airline_code = airline_code_table.get(airline.text)
        price = element.find('span', class_=starts('avg-price-txt'))
        depart, arrive = element.find_all('span', class_=starts('time'))
        depart_date = depart['data-testid'].split()[0][-10:]
        
        duration = element.find('div', class_=starts('flight-info-duration_'))
        dairport,aairport = element.find_all('div', class_=starts('flt-card-stop__code'))
        baggage_element = element.find_all('i', class_='fi-icon')
        bags = [item['data-label-track'] for item in baggage_element]
        FREE_CHECKED_BAGGAGE = 'Yes' if len(baggage_element) >= 1 else 'No'
        FREE_CARRY_ON_BAGGAGE = 'NA'

        if airline_code is not None:
            data.append([datetime.now().strftime('%Y-%m-%d'),
                            depart_date,
                            airline.text, 
                            airline_code,
                            price.text.split('HK$')[-1] if 'HK$' in price.text else price.text, 
                            depart.text, 
                            arrive.text,
                            duration.text,
                            dairport.text[:3],
                            aairport.text[:3],
                            FREE_CHECKED_BAGGAGE,
                            FREE_CARRY_ON_BAGGAGE])
            print(data[-1])

    with open(f'flight_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

if __name__ == "__main__":
    run()



