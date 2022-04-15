import requests
from bs4 import BeautifulSoup
import multiprocessing
import asyncio
import aiohttp


# Global parse variables (constants)
url = 'https://someurl.com/data-list/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
}
params = {
    'count': '100',
    'scrIds': 'day_gainers',
}


def parse_result_handle(response):
    print(response)
    # Handling the response here


# Coroutine where single page is being parsed
async def parse_coroutine(page: int, session: aiohttp.ClientSession) -> list:
    # Sending http get request and serializing the response
    async with session.get(f'{url}&page={page}',headers=headers, params=params) as response:
        # Handling parsed data here
        html = BeautifulSoup(await response.text(), 'html.parser')
        items = html.find_all('some', class_='some_class')
        return [{} for item in items]


# Gathering parsed pages data of page range
async def parse_gather(pages: tuple) -> tuple:
    # Opening http connection session
    async with aiohttp.ClientSession() as session:
        # Filling the tasks list with coroutines
        tasks = []
        [tasks.append(
            asyncio.create_task(parse_coroutine(page, session))
        ) for page in range(*pages)]
        return await asyncio.gather(*tasks)


# Process parsing function for parallel execution (process target)
def parse_pages(pages: tuple) -> list:
    # Avoiding 'RuntimeError: Event loop is closed'
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    data = asyncio.run(parse_gather(pages))
    return data

# Main function managing parallel execution
def parse(pages_amount: int = 50) -> None:
    # Creating jobs for concurrent execution
    threads_amount = multiprocessing.cpu_count()
    pages_per_process = int(pages_amount / threads_amount)
    pages_left = pages_amount % threads_amount
    jobs = []
    first_page = 0
    # Filing the jobs with page ranges (start, end)
    for _ in range(threads_amount):
        job_pages_amount = pages_per_process + 1 if pages_left else pages_per_process
        if job_pages_amount:
            jobs.append((first_page, first_page + job_pages_amount))
        else:
            break
        pages_left -= 1
        first_page += job_pages_amount
    # Test request to check for exceptions
    response = requests.get(url, headers=headers, params={})
    if response.status_code == 200:
        # Initializing process pool
        with multiprocessing.Pool(threads_amount) as pool:
            pool.map_async(parse_pages, jobs, callback=parse_result_handle)
            pool.close()
            pool.join()
    else:
        # Bad request error handling here
        print(f'Parsing error. Http request status code is {response.status_code}')


if __name__ == '__main__':
    parse(70)
