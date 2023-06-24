import asyncio
import requests
import json
from aiohttp import ClientSession
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

final_data = []

async def fetch(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            try:
                response_content = await response.content.read()
                soup = BeautifulSoup(response_content, "html.parser")
                table = soup.find("table", class_="cmc-table")
                rows = table.find_all("tr")
                for row in rows[1:11]:
                    try:
                        columns = row.find_all("td")

                        name_element = columns[2].find("p")
                        name = name_element.text.strip() if name_element else "N/A"

                        price = columns[3].text.strip()
                        percent_1h = columns[4].text.strip()
                        percent_24h = columns[5].text.strip()
                        percent_7d = columns[6].text.strip()
                        market_cap = columns[7].text.strip()
                        volume_24h = columns[8].text.strip()
                        circulating_supply = columns[9].text.strip()

                        final_data.append(
                            {
                                'name': name,
                                'price': price,
                                '1h': percent_1h,
                                '24h': percent_24h,
                                '7d': percent_7d,
                                'market_cap': market_cap,
                                'volume(24h)': volume_24h,
                                'circulating supply': circulating_supply,
                            }
                        )
                    except Exception as e:
                        print(f"Error while parsing row: {e}")
            except Exception as e:
                print(f"Error while fetching URL: {e}")
            return True



async def main():
    final_data.clear()
    d1 = datetime.now()
    tasks = []
    for page in range(1, 11):
        url = f"https://coinmarketcap.com/?page={page}"
        tasks.append(fetch(url))
    await asyncio.gather(*tasks)
    headers = {'Content-Type': 'application/json'}
    url1 = 'http://127.0.0.1:5000/cryptos'
    response = requests.post(url1, data=json.dumps(final_data), headers=headers)
    print(response)
    d2 = datetime.now()
    print(d2 - d1)
    print(len(final_data))


async def run_webscraper():
    while True:
        d1 = datetime.now()
        await main()
        d2 = datetime.now()
        elapsed_time = d2 - d1
        if elapsed_time < timedelta(seconds=5):
            await asyncio.sleep(5 - elapsed_time.total_seconds())


# Entry point
if __name__ == "__main__":
    asyncio.run(run_webscraper())
