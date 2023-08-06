import requests
from bs4 import BeautifulSoup
from .utils import convert_str_to_number, ThreadWithReturnValue as Thread
import asyncio
import aiohttp


URL = 'https://habr.com/'


def get_posts_links_from_page(page: str = None, en: bool = False, hub: str = None, search: str = None) -> list:
    """ Returns list containing links to posts from page """

    # check args
    if search is not None and hub is not None:
        raise RuntimeError('Do not use hub with search')

    # formation of the final url
    final_url = URL
    if en:
        final_url += 'en/'
    else:
        final_url += 'ru/'
    if hub is not None:
        final_url += 'hub/' + hub + '/'
    if search is not None:
        final_url += 'search/'
    if page is not None:
        final_url += page + '/'
    if search is not None:
        final_url += '?q=' + search

    # trying to get the page
    response = requests.get(final_url)
    if response.status_code != 200:
        print(f'Response status code is {response.status_code}')
        return None

    # passing response to bs and getting links to posts
    page = BeautifulSoup(response.text, 'lxml')
    posts = page.find_all('a', class_='post__habracut-btn')
    result = list()
    for post in posts:
        result.append(post['href'])
    return result


def get_hub(href: str) -> dict:
    """ Return some information about the hub """

    # trying to get the hub
    response = requests.get(href)
    if response.status_code != 200:
        print(f'Response status code is {response.status_code}')
        return None

    # passing response to bs
    hub = BeautifulSoup(response.text, 'lxml')

    # trying to get icon of hub
    pic = None
    try:
        pic = 'https:' + hub.select_one('.media-obj__image-pic')['src']
    except TypeError:
        pass

    # get all other information
    result = {
        'name': getattr(hub.select_one('.page-header__info-title'), "text", ""),
        'link': href,
        'desc': getattr(hub.select_one('.page-header__info-desc'), "text", ""),
        'pic': pic,
    }
    return result


def get_hubs(en: bool = False, page: str = None) -> list:
    """ Returns lists of hubs from habr.com/hubs """

    # formation of the final url
    if en:
        final_url = 'https://habr.com/en/hubs/'
    else:
        final_url = 'https://habr.com/ru/hubs/'
    if page is not None:
        final_url += page

    # trying to get the page
    response = requests.get(final_url)
    if response.status_code != 200:
        print(f'Response status code is {response.status_code}')
        return None

    # passing response to bs and getting links to hubs
    page = BeautifulSoup(response.text, 'lxml')
    hubs = page.find_all('li', class_='content-list__item_hubs')

    # get information about hubs using bs
    result = list()
    for hub in hubs:
        hub_name = hub.find('a', class_='list-snippet__title-link').text
        hub_link = hub.find('a', class_='list-snippet__title-link')['href']
        hub_pic = 'https:' + hub.find('img', class_='media-obj__image-pic media-obj__image-pic_hub')['src']
        hub_desc = hub.find('div', class_='list-snippet__desc').text
        hub_tags = hub.find('div', class_='list-snippet__tags')
        if hub_tags is not None:
            hub_tags = hub_tags.find_all('a')
            for i in range(len(hub_tags)):
                hub_tags[i] = {
                    'name': hub_tags[i].text,
                    'link': hub_tags[i]['href'],
                }
        result.append(dict(name=hub_name, link=hub_link, pic=hub_pic, desc=hub_desc, tags=hub_tags))
    return result


def get_post(href: str, session: requests.sessions.Session = requests.Session(), full: bool = False) -> dict:
    """ Retusn some information about the post """
    # trying to get the page
    response = session.get(href)
    if response.status_code != 200:
        print(f'Response status code is {response.status_code}')
        return None

    # passing response to bs
    post = BeautifulSoup(response.text, 'lxml')

    # getting post's hubs
    hubs_bs = post.find_all('a', class_='hub-link')  # list of bs objects
    hubs = list()  # dicts created using get_hub
    for hub in hubs_bs:
        hubs.append(get_hub(hub['href']))

    # getting post's tags
    tags_bs = post.find_all('a', class_='post__tag')  # list of bs objects
    tags = list()  # dict created by 'for' loop below
    for tag in tags_bs:
        if tag.has_attr('href'):
            tags.append({'name': tag.text, 'link': tag['href']})

    # getting information about post using bs
    result = {
        'title': post.find('h1').text,
        'link': href,
        'hubs': hubs,
        'tags': list(filter(lambda t: not list(filter(lambda h: h['link'] == t['link'], hubs)), tags)),  # hubs also icnlude class post__tag so i need to exclude tags that have the same link as hubs
        'score': convert_str_to_number(getattr(post.find('span', class_='voting-wjt__counter'), "text", "0")),  # score is getting in format like '21k' so i need to transform this string ro number, it also can does not exists if posts does not have score
        'views': convert_str_to_number(getattr(post.find('span', class_='post-stats__views-count'), "text", "0")),  # same as above
        'bookmarked': convert_str_to_number(getattr(post.find('span', class_='bookmark__counter'), "text", "0")),  # same as above
        'comments': convert_str_to_number(getattr(post.find('span', class_='post-stats__comments-count'), "text", "0")),  # same as above
    }
    if full:  # if you need body of the post (post's content) you can pass 'full' parameter
        result['body'] = str(post.find('div', class_='post__body post__body_full'))  # bs functions return bs object so i need to transform it to string
    return result


async def get_post_async(href: str, session: aiohttp.client.ClientSession = aiohttp.ClientSession(), full: bool = False):
    """ Same as get_post but async """

    # trying to get the page
    response = await session.get(href)
    if response.status != 200:
        print(f'Response status code is {response.status_code}')
        return None

    # passing response to bs
    respone_text = await response.text()
    post = BeautifulSoup(respone_text, 'lxml')

    # getting post's hubs
    hubs_bs = post.find_all('a', class_='hub-link')  # list of bs objects
    hubs = list()  # dicts created using get_hub
    for hub in hubs_bs:
        hubs.append(get_hub(hub['href']))

    # getting post's tags
    tags_bs = post.find_all('a', class_='post__tag')  # list of bs objects
    tags = list()  # dict created by 'for' loop below
    for tag in tags_bs:
        if tag.has_attr('href'):
            tags.append({'name': tag.text, 'link': tag['href']})

    # getting information about post using bs
    result = {
        'title': post.find('span', class_='post__title-text').text,
        'link': href,
        'hubs': hubs,
        'tags': list(filter(lambda t: not list(filter(lambda h: h['link'] == t['link'], hubs)), tags)),  # hubs also icnlude class post__tag so i need to exclude tags that have the same link as hubs
        'score': convert_str_to_number(getattr(post.find('span', class_='voting-wjt__counter'), "text", "0")),  # score is getting in format like '21k' so i need to transform this string ro number, it also can does not exists if posts does not have score
        'views': convert_str_to_number(getattr(post.find('span', class_='post-stats__views-count'), "text", "0")),  # same as above
        'bookmarked': convert_str_to_number(getattr(post.find('span', class_='bookmark__counter'), "text", "0")),  # same as above
        'comments': convert_str_to_number(getattr(post.find('span', class_='post-stats__comments-count'), "text", "0")),  # same as above
    }
    if full:  # if you need body of the post (post's content) you can pass 'full' parameter
        result['body'] = str(post.find('div', class_='post__body post__body_full'))  # bs functions return bs object so i need to transform it to string
    return result


async def get_posts_from_page_async(page: str = None, en: bool = False, hub: str = None, search: str = None):
    """ Same as get_post_from_page but async """

    # get links to posts
    posts_links = get_posts_links_from_page(page=page, en=en, hub=hub, search=search)

    # if there are no links on page return None
    if posts_links is None:
        return None

    # formation of tasks
    tasks = list()
    async with aiohttp.ClientSession() as session:
        for post_link in posts_links:
            task = asyncio.ensure_future(get_post_async(post_link, session))
            tasks.append(task)
        posts = await asyncio.gather(*tasks)
    return posts


def get_posts_from_page_multithreading(page: str = None, en: bool = False, hub: str = None, search: str = None) -> list:
    """ Same as get_post_from_page but using threads """

    # get links to posts
    posts_links = get_posts_links_from_page(page=page, en=en, hub=hub, search=search)

    # if there are no links on page return None
    if posts_links is None:
        return None

    # getting information about posts using get_post and threads
    posts = list()
    session = requests.Session()
    for post_link in posts_links:
        posts.append(Thread(target=get_post, args=(post_link, session)))
    for post in posts:
        post.start()
    for i in range(len(posts)):
        posts[i] = posts[i].join()
    return posts


def get_posts_from_page(page: str = None, en: bool = False, hub: str = None, search: str = None) -> list:
    """ Returns information about all posts on page using get_posts_links_from_page and get_post """

    # get links to posts
    posts_links = get_posts_links_from_page(page=page, en=en, hub=hub, search=search)

    # if there are no links on page return None
    if posts_links is None:
        return None

    # getting information about posts using get_post
    posts = list()
    session = requests.Session()
    for post_link in posts_links:
        posts.append(get_post(post_link, session))
    return posts


def check_next_page_exists(en: bool = False, page: str = 'page1', hub: str = None, search: str = None, hubs: bool = False):
    """ Returns True if next page exists and False if it does not """

    # check args
    if search is not None and hub is not None:
        raise RuntimeError('Do not use hub with search')
    if search is not None and hubs:
        raise RuntimeError('Do not use hubs with search')
    if hub is not None and hubs:
        raise RuntimeError('Do not use hubs with hub')

    # formation of the final url
    final_url = URL
    if en:
        final_url += 'en/'
    else:
        final_url += 'ru/'
    if hub is not None:
        final_url += 'hub/' + hub + '/'
    if hubs:  # if you need to check in next page in hubs exists set hubs (like habr.com/hubs/page2)
        final_url += 'hubs/'
    if page is not None:
        final_url += page + '/'
    if search is not None:
        final_url += '?q=' + search

    # trying to get the page
    response = requests.get(final_url)

    # if page does not exists next page can not exists
    if response.status_code != 200:
        print(f'Response status code is {response.status_code}')
        return False

    # passing response to bs
    page = BeautifulSoup(response.text, 'lxml')
    # trying to find link to next page
    next_page = page.select_one('.arrows-pagination__item-link.arrows-pagination__item-link_next')
    if next_page is None:   # if it does not exists next page does not exists
        return False
    return True
