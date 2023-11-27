import json
import re
import requests
from bs4 import BeautifulSoup

base_link = "https://rocketleague.tracker.network/rocket-league/distribution?playlist="

modes = {
    "1v1": 10,
    "2v2": 11,
    "3v3": 12,
    "3v3s": 13,
    "hoops": 27,
    "rumble": 28,
    "dropshot": 29,
    "snowday": 30,
}


def get_links(modes, base_link):
    links = {}
    for mode in modes:
        links[mode] = base_link + str(modes[mode])
    return links


links = get_links(modes, base_link)


def clean_players_data(players_data):
    cleaned_data = re.sub(r" players.*$", "", players_data)
    cleaned_data = re.sub(r"[\s,]+", "", cleaned_data)
    return cleaned_data


def clean_divisions_data(divisions_data):
    cleaned_data = re.sub(r"\u2014", "-", divisions_data)
    return cleaned_data


def scrape_with_xpath(links, xpath_mode, xpath_value, xpath_divisions):
    data_list = []

    for mode, url in links.items():
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            mode_elements = soup.select(xpath_mode)
            mode_data = [element.text for element in mode_elements]

            value_elements = soup.select(xpath_value)
            value_data = [
                clean_players_data(element.text) for element in value_elements
            ]

            mode_values = [
                {"rank": mode_rank, "players": mode_players}
                for mode_rank, mode_players in zip(mode_data, value_data)
            ]

            for i, xpath_division in enumerate(xpath_divisions, start=1):
                division_elements = soup.select(xpath_division)
                division_values = [
                    clean_divisions_data(element.text) for element in division_elements
                ]

                for j, mode_value in enumerate(mode_values):
                    mode_value[f"division_{i}"] = (
                        division_values[j] if j < len(division_values) else ""
                    )

            data_list.append({"mode": mode, "values": mode_values})
        else:
            print(f"Failed to retrieve the page for URL: {url}")

    return data_list


xpath_mode_expression = ".tier .name"
xpath_value_expression = ".metadata"
xpath_divisions_expressions = [
    "td:nth-child(2)",
    "td:nth-child(3)",
    "td:nth-child(4)",
    "td:nth-child(5)",
]

result_list = scrape_with_xpath(
    links, xpath_mode_expression, xpath_value_expression, xpath_divisions_expressions
)

result_json = json.dumps(result_list, indent=2)


with open("distributions.json", "w") as outfile:
    json.dump(result_list, outfile)
