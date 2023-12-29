from bs4 import BeautifulSoup
from dataclasses import dataclass
import json
import asyncio
from pyppeteer import launch

@dataclass
class Item:
    sport_league: str = ''
    event_date_utc: str = ''
    team1: str = ''
    team2: str = ''
    pitcher: str = ''
    period: str = ''
    line_type: str = ''
    price: str = ''
    side: str = ''
    team: str = ''
    spread: float = 0.0

async def fetch_data():
    url = "https://veri.bet/odds-picks?filter=upcoming"
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    await page.waitForSelector('.event', {'timeout': 300000})

    await asyncio.sleep(10)

    content = await page.content()
    await browser.close()
    return content

def parse_veri_bet(content):
    soup = BeautifulSoup(content, 'html.parser')

    parsed_data = []

    for event in soup.find_all('div', class_='event'):
        sport_league = event['data-sport']
        event_date_utc = event['data-event-date']
        team1 = event['data-team1']
        team2 = event['data-team2']
        pitcher = event['data-pitcher']
        period = event['data-period']

        for bet_type in event.find_all('div', class_='bet-type'):
            line_type = bet_type['data-line-type']
            price = bet_type['data-price']
            side = bet_type['data-side']
            team = bet_type['data-team']
            spread = float(bet_type['data-spread']) if 'data-spread' in bet_type.attrs else 0.0

            item = Item(sport_league, event_date_utc, team1, team2, pitcher, period, line_type, price, side, team, spread)
            parsed_data.append(item)

    return parsed_data

def main():
    loop = asyncio.get_event_loop()
    content = loop.run_until_complete(fetch_data())
    parsed_data = parse_veri_bet(content)
    json_data = json.dumps([item.__dict__ for item in parsed_data], indent=2)
    print(json_data)

if __name__ == "__main__":
    main()
