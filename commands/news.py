from bs4 import BeautifulSoup
import requests
import random
import discord

page_num = random.randint(1, 10)
url = f'https://www.delfi.ee/viimased?page={page_num}'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

div_banners = soup.find_all('div', {'class': 'C-block-type-6 C-headline-list__headline C-block-type-6--separated'})

def image_url_delfi(url):
    urly = f'{url}'
    response = requests.get(urly)
    soup = BeautifulSoup(response.content, 'html.parser')

    div_banners = soup.find_all('div', {'class': 'C-lazy-image'})

    for div_banner in div_banners:
        a_element = div_banner.find('img')
        if 'src' in a_element.attrs:
            news_url = a_element['src']
            return news_url
        
def image_url_postimees(url):
    urly = f'{url}'
    response = requests.get(urly)
    soup = BeautifulSoup(response.content, 'html.parser')

    div_banners = soup.find_all('img', {'class': 'figure__image'})

    for div_banner in div_banners:
            news_url = div_banner['src']
            return news_url

def headline_postimees(url):
    urly = f'{url}'
    response = requests.get(urly)
    soup = BeautifulSoup(response.content, 'html.parser')

    div_banners = soup.find_all('span', {'class': 'article__headline--exclamation'})

    for div_banner in div_banners:
            news_url = div_banner['span']
            return news_url
    
async def news_postimees(ctx):
    url = 'https://www.postimees.ee/latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    all_links = soup.find_all('a', {'class': 'list-article__url'})
    if len(all_links) > 0:
        random_link = random.choice(all_links)
        if 'href' in random_link.attrs:
            href = random_link['href']
        image_urls = image_url_postimees(href)
        news = discord.Embed(title="Postimees", description=href, color=discord.Color.gold())
        news.set_image(url="https://f12.pmo.ee/quzPCS8ney-Vpz-Vz5hGm_ubbpo=/155x155/smart/nginx/o/2022/03/07/14411686t1hca79.png")
        await ctx.send(embed=news)


async def news_delfi(ctx):
    if len(div_banners) > 0:
        div_banner = random.choice(div_banners)
        a_element = div_banner.find('a')
        if 'href' in a_element.attrs:
            urlss = a_element['href']
        image_urls = image_url_delfi(urlss)
        news = discord.Embed(title="Delfi", description=urlss, color=discord.Color.gold())
        news.set_image(url=image_urls)
        await ctx.send(embed=news)