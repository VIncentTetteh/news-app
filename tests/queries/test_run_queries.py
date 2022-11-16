import responses

from src.queries.run_queries import QueryManager
from src.utils.external_libs_config import (
    API_COLLECTION,
    EXTERNAL_SOURCES_CONFIG,
    NEWS_API_CONFIG,
    REDDIT_API_CONFIG,
)


@responses.activate
def test_get_news_query_new_api_success():

    manager = QueryManager(limit=2)
    expected_response = {
        "articles": [
            {
                "source": {"id": "cnn", "name": "CNN"},
                "author": "Chuck Johnston, CNN",
                "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
                "description": "Officers located at least 15 shooting victims, including 6 who are deceased, Sacramento police said Sunday morning.",
                "url": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
                "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/220403081633-02-sacramento-shooting-0403-super-tease.jpg",
                "publishedAt": "2022-04-03T12:33:00Z",
            },
            {
                "source": {"id": None, "name": "New York Times"},
                "author": "Christina Goldbaum, Salman Masood",
                "title": "Imran Khan Live Updates: Pakistan Parliament News and the Latest - The New York Times",
                "description": "It was not clear whether Imran Khan’s maneuver would succeed, and it seemed to raise the possibility.",
                "url": "https://www.nytimes.com/live/2022/04/03/world/imran-khan-confidence-vote-pakistan",
                "urlToImage": "https://static01.nyt.com/images/2022/04/03/world/03pakistan-khan-header/03pakistan-khan-header-facebookJumbo.jpg",
                "publishedAt": "2022-04-03T12:29:01Z",
            },
        ]
    }

    expected_result = [
        {
            "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
            "link": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
            "source": "newsapi",
        },
        {
            "title": "Imran Khan Live Updates: Pakistan Parliament News and the Latest - The New York Times",
            "link": "https://www.nytimes.com/live/2022/04/03/world/imran-khan-confidence-vote-pakistan",
            "source": "newsapi",
        },
    ]

    responses.add(
        responses.GET,
        EXTERNAL_SOURCES_CONFIG[NEWS_API_CONFIG]["listing_url"].format(limit=2),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"x-api-key": EXTERNAL_SOURCES_CONFIG[NEWS_API_CONFIG]["access_key"]},
    )

    result = manager.get_news_query()
    assert expected_result == result
    assert 2 == len(result)


@responses.activate
def test_get_news_query_new_api_error():
    """Passing a library that doesn't exit"""

    TWITTER_API_CONFIG = 0

    UNREGISTERED_LIBRARY = {
        TWITTER_API_CONFIG: {
            "api_name": "test",
            "source": "test",
            "listing_url": "http://twitter.com/pageSize={limit}&page=1",
            "search_url": "http://twitter?q='{query}'&pageSize='{limit}'&page=1",
        }
    }

    manager = QueryManager(limit=2)
    expected_response = {
        "articles": [
            {
                "source": {"id": "cnn", "name": "CNN"},
                "author": "Chuck Johnston, CNN",
                "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
                "description": "Officers located at least 15 shooting victims, including 6 who are deceased, Sacramento police said Sunday morning.",
                "url": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
                "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/220403081633-02-sacramento-shooting-0403-super-tease.jpg",
                "publishedAt": "2022-04-03T12:33:00Z",
                "content": None,
            },
            {
                "source": {"id": None, "name": "New York Times"},
                "author": "Christina Goldbaum, Salman Masood",
                "title": "Imran Khan Live Updates: Pakistan Parliament News and the Latest - The New York Times",
                "description": "It was not clear whether Imran Khan’s maneuver would succeed, and it seemed to raise the possibility of a constitutional crisis. Stunned opposition lawmakers said they would turn to the Supreme Court.",
                "url": "https://www.nytimes.com/live/2022/04/03/world/imran-khan-confidence-vote-pakistan",
                "urlToImage": "https://static01.nyt.com/images/2022/04/03/world/03pakistan-khan-header/03pakistan-khan-header-facebookJumbo.jpg",
                "publishedAt": "2022-04-03T12:29:01Z",
                "content": "The Darul Uloom Haqqania madrasa in Akhora Khattak, Pakistan, has educated more Taliban leaders than any school in the world.Credit...Saiyna Bashir for The New York Times\r\nISLAMABAD, Pakistan Pakista… [+3506 chars]",
            },
        ]
    }

    responses.add(
        responses.GET,
        UNREGISTERED_LIBRARY[TWITTER_API_CONFIG]["listing_url"].format(limit=2),
        json=expected_response,
        status=400,
        content_type="application/json",
        headers={"x-api-key": ""},
    )

    actual_response = []

    assert actual_response == manager.get_news_query()


@responses.activate
def test_get_news_query_reddit_api_success():

    manager = QueryManager(limit=2)
    expected_response = {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
                        "url": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
                    },
                },
                {
                    "kind": "t4",
                    "data": {
                        "title": "Estelle Harris Dies: Seinfeld’s Estelle Costanza, Toy Story",
                        "url": "https://deadline.com/2022/04/estelle-harris-dead-seinfelds-estelle-costanza-was-93-1234993091/",
                    },
                },
            ]
        }
    }

    expected_result = [
        {
            "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
            "link": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
            "source": "reddit",
        },
        {
            "title": "Estelle Harris Dies: Seinfeld’s Estelle Costanza, Toy Story",
            "link": "https://deadline.com/2022/04/estelle-harris-dead-seinfelds-estelle-costanza-was-93-1234993091/",
            "source": "reddit",
        },
    ]

    responses.add(
        responses.GET,
        EXTERNAL_SOURCES_CONFIG[REDDIT_API_CONFIG]["listing_url"].format(limit=2),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"User-agent": "your bot 0.1"},
    )

    result = manager.get_news_query()
    assert expected_result == result
    assert 2 == len(result)


@responses.activate
def test_get_news_query_reddit_api_error():
    """Passing a library that doesn't exit"""

    TWITTER_API_CONFIG = 0

    UNREGISTERED_LIBRARY = {
        TWITTER_API_CONFIG: {
            "api_name": "test",
            "source": "test",
            "listing_url": "http://twitter.com/pageSize={limit}&page=1",
            "search_url": "http://twitter?q='{query}'&pageSize='{limit}'&page=1",
        }
    }

    manager = QueryManager(limit=2)
    expected_response = {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
                        "url": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
                    },
                },
                {
                    "kind": "t4",
                    "data": {
                        "title": "Estelle Harris Dies: Seinfeld’s Estelle Costanza, Toy Story",
                        "url": "https://deadline.com/2022/04/estelle-harris-dead-seinfelds-estelle-costanza-was-93-1234993091/",
                    },
                },
            ]
        }
    }

    expected_result = [
        {
            "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
            "link": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
            "source": "reddit",
        },
        {
            "title": "Estelle Harris Dies: Seinfeld’s Estelle Costanza, Toy Story",
            "link": "https://deadline.com/2022/04/estelle-harris-dead-seinfelds-estelle-costanza-was-93-1234993091/",
            "source": "reddit",
        },
    ]

    responses.add(
        responses.GET,
        UNREGISTERED_LIBRARY[TWITTER_API_CONFIG]["listing_url"].format(limit=2),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"User-agent": "your bot 0.1"},
    )

    result = manager.get_news_query()
    assert [] == result
    assert 0 == len(result)


@responses.activate
def test_search_news_query_new_api_success():
    query_params = "wounded"
    manager = QueryManager(query=query_params, limit=2)
    expected_response = {
        "articles": [
            {
                "source": {"id": "cnn", "name": "CNN"},
                "author": "Chuck Johnston, CNN",
                "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
                "description": "Officers located at least 15 shooting victims, including 6 who are deceased, Sacramento police said Sunday morning.",
                "url": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
                "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/220403081633-02-sacramento-shooting-0403-super-tease.jpg",
                "publishedAt": "2022-04-03T12:33:00Z",
                "content": None,
            },
        ]
    }

    expected_result = [
        {
            "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
            "link": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
            "source": "newsapi",
        }
    ]

    responses.add(
        responses.GET,
        EXTERNAL_SOURCES_CONFIG[NEWS_API_CONFIG]["search_url"].format(
            query=query_params, limit=2
        ),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"x-api-key": EXTERNAL_SOURCES_CONFIG[NEWS_API_CONFIG]["access_key"]},
    )

    result = manager.search_news_query()
    assert expected_result == result
    assert 1 == len(result)


@responses.activate
def test_search_news_query_new_api_failure():
    """Passing a library that doesn't exit"""

    TWITTER_API_CONFIG = 0

    UNREGISTERED_LIBRARY = {
        TWITTER_API_CONFIG: {
            "api_name": "test",
            "source": "test",
            "listing_url": "http://twitter.com/pageSize={limit}&page=1",
            "search_url": "http://twitter?q='{query}'&pageSize='{limit}'&page=1",
        }
    }
    query_params = "wounded"
    manager = QueryManager(query=query_params, limit=2)
    expected_response = {
        "articles": [
            {
                "source": {"id": "cnn", "name": "CNN"},
                "author": "Chuck Johnston, CNN",
                "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
                "description": "Officers located at least 15 shooting victims, including 6 who are deceased, Sacramento police said Sunday morning.",
                "url": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
                "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/220403081633-02-sacramento-shooting-0403-super-tease.jpg",
                "publishedAt": "2022-04-03T12:33:00Z",
                "content": None,
            },
        ]
    }

    expected_result = [
        {
            "title": "6 people are dead and at least 9 others are wounded after a shooting in downtown Sacramento - CNN",
            "link": "https://www.cnn.com/2022/04/03/us/sacramento-california-shooting/index.html",
            "source": "newsapi",
        }
    ]

    responses.add(
        responses.GET,
        UNREGISTERED_LIBRARY[TWITTER_API_CONFIG]["search_url"].format(
            query=query_params, limit=2
        ),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"x-api-key": EXTERNAL_SOURCES_CONFIG[NEWS_API_CONFIG]["access_key"]},
    )

    result = manager.search_news_query()
    assert [] == result
    assert 0 == len(result)


@responses.activate
def test_search_news_query_reddit_api_success():
    query_params = "mutilate"
    manager = QueryManager(query=query_params, limit=2)
    expected_response = {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
                        "url": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
                    },
                }
            ]
        }
    }

    expected_result = [
        {
            "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
            "link": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
            "source": "reddit",
        }
    ]

    responses.add(
        responses.GET,
        EXTERNAL_SOURCES_CONFIG[REDDIT_API_CONFIG]["search_url"].format(
            query=query_params, limit=2
        ),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"User-agent": "your bot 0.1"},
    )

    result = manager.search_news_query()
    assert expected_result == result
    assert 1 == len(result)


@responses.activate
def test_search_news_query_reddit_api_failure():
    """Passing a library that doesn't exit"""

    TWITTER_API_CONFIG = 0

    UNREGISTERED_LIBRARY = {
        TWITTER_API_CONFIG: {
            "api_name": "test",
            "source": "test",
            "listing_url": "http://twitter.com/pageSize={limit}&page=1",
            "search_url": "http://twitter?q='{query}'&pageSize='{limit}'&page=1",
        }
    }
    query_params = "mutilate"
    manager = QueryManager(query=query_params, limit=2)
    expected_response = {
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
                        "url": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
                    },
                }
            ]
        }
    }

    expected_result = [
        {
            "title": "They said they’d mutilate and kill me,’ says kidnapped Ukrainian journalist",
            "link": "https://www.theguardian.com/world/2022/apr/03/they-said-theyd-mutilate-and-kill-me-says-kidnapped-ukrainian-journalist",
            "source": "reddit",
        }
    ]

    responses.add(
        responses.GET,
        UNREGISTERED_LIBRARY[TWITTER_API_CONFIG]["search_url"].format(
            query=query_params, limit=2
        ),
        json=expected_response,
        status=200,
        content_type="application/json",
        headers={"User-agent": "your bot 0.1"},
    )

    result = manager.search_news_query()
    assert [] == result
    assert 0 == len(result)