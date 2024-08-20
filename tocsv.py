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

    for element in elements_with_index:
       #try:
            
            airline = element.find('div', class_ = 'flights-name')
            price = element.find('span', class_=starts('o-price-flight'))
            depart, arrive = element.find_all('span', class_=starts('time'))
            depart_date = depart['data-testid'].split()[0][-10:]
            
            duration = element.find('div', class_=starts('flight-info-duration_'))
            dairport,aairport = element.find_all('span', class_=starts('flight-info-stop__code_'))
            baggage_element = element.find_all('i', class_='baggage-icon')
            bags = [item['data-label-track'] for item in baggage_element]
            FREE_CHECKED_BAGGAGE = 'FREE_CHECKED_BAGGAGE' if 'FREE_CHECKED_BAGGAGE' in bags else ''
            FREE_CARRY_ON_BAGGAGE = 'FREE_CARRY_ON_BAGGAGE' if 'FREE_CARRY_ON_BAGGAGE' in bags else ''
            data.append([datetime.now().strftime('%Y%m%d.%H'),
                         depart_date,
                         airline.text, 
                         price['data-price'], 
                         depart.text, 
                         arrive.text,
                         duration.text,
                         dairport.text[:3],
                         aairport.text[:3],
                         FREE_CHECKED_BAGGAGE,
                         FREE_CARRY_ON_BAGGAGE])
            print(data[-1])
        #except:
            #print('incomplete loading')
    with open(f'flight_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

if __name__ == "__main__":
    run()



