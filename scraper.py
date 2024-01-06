import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_pharmeasy(letter):
    medicine_data = []
    for page in range(12):
        url = f"https://pharmeasy.in/online-medicine-order/browse?alphabet={letter}&page={page}"
        print(url)
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        medicine_containers = soup.find_all("div", class_="BrowseList_medicineContainer__Fi9u7")
        for container in medicine_containers:
            medicine_url = "https://pharmeasy.in" + container.find("a", class_="BrowseList_medicine__cQZkc")["href"]
            data = scrape_pharmeasy_data(medicine_url)
            medicine_data.append(data)
    df = pd.DataFrame(medicine_data)
    print(df.shape)
    df.to_excel('Pharmeasy_f.xlsx', index=False)

def scrape_pharmeasy_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        name = soup.find("h1", class_="MedicineOverviewSection_medicineName__dHDQi").text.strip()
    except AttributeError:
        name = "Not Found"

    try:
        quantity = soup.find("div", class_="MedicineOverviewSection_measurementUnit__7m5C3").text.strip()
    except AttributeError:
        quantity = "Not Found"

    try:
        manufacturer = soup.find("div", class_="MedicineOverviewSection_brandName__rJFzE").text.strip()
    except AttributeError:
        manufacturer = "Not Found"

    try:
        mrp = soup.find("span", class_="PriceInfo_striked__Hk2U_").text.strip()
    except AttributeError:
        mrp = "Not Found"

    try:
        discounted_price = soup.find("div", class_="PriceInfo_gcdDiscountContainer__hr0YD").find("span").text.strip()
    except AttributeError:
        discounted_price = "Not Found"

    try:
        salt = soup.find("td", {"class": "DescriptionTable_field__l5jJ3"}, text="Contains").find_next("td", class_="DescriptionTable_value__0GUMC").text.strip()
    except AttributeError:
        salt = "Not Found"
        
    return {
            'Name': name,
            'MRP': mrp,
            'Discounted Price': discounted_price,
            'Quantity': quantity,
            'Salt': salt,
            'Manufacturer': manufacturer,
            'URL': url
        }
    
def scrape_netmeds():
    url = "https://www.netmeds.com/prescriptions"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.select('.alpha-drug-list a')
    urls=[]
    hrefs=[]
    medicine_data = []
    for category in categories:
        medicine_url = "https://www.netmeds.com/prescriptions/" + category.text.strip().split('(')[0].strip().replace(' ', '-').replace('/', '-').replace('.','-').replace('---','-').lower()  
        urls.append(medicine_url)
    for urly in urls:
        response = requests.get(urly)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.product-item a')
        for link in links:
            h=link.get('href')
            href = h.split('https://www.netmeds.com/prescriptions/')[1]
            if href.startswith('b') or href.startswith('f'):
                if len(hrefs) >= 2000:
                    break
                hrefs.append(h)
    for href in hrefs:
        data=scrape_netmeds_data(href)
        medicine_data.append(data)
    df = pd.DataFrame(medicine_data)
    print(df.shape)
    df.to_excel('Netmeds.xlsx', index=False)

def scrape_netmeds_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    try:
        name_element = soup.find('h1', class_='black-txt')
        medicine_name = name_element.text.strip()
    except AttributeError:
        medicine_name = "Not Found"

    try:
        mrp_element = soup.find('span', class_='final-price')
        mrp = mrp_element.text.strip().replace('MRP', '', 1).strip()
    except AttributeError:
        mrp = "Not Found"

    try:
        discounted_price_element = soup.find('span', id='barBestPrice')
        discounted_price = discounted_price_element.text.strip()
    except AttributeError:
        discounted_price = "Not Found"

    try:
        quantity_element = soup.find('span', class_='drug-varient')
        quantity = quantity_element.text.strip().replace('*', '', 1)
    except AttributeError:
        quantity = "Not Found"

    try:
        manufacturer_element = soup.find('span', class_='drug-manu')
        manufacturer = manufacturer_element.text.strip().split(':', 1)[-1].strip()
    except AttributeError:
        manufacturer = "Not Found"

    return {
        'Medicine Name': medicine_name,
        'MRP': mrp,
        'Discounted Price': discounted_price,
        'Quantity': quantity,
        'Manufacturer': manufacturer,
        'URL': url
    }
