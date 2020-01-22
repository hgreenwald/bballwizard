"""
The goal of this file is to hold all the functions to scrape game data from https://www.basketball-reference.com/.
We'll be using this data to build our basic bayesian model around the five factors: eFG%, TOV%, ORB%, FT/FGA, ORtg
"""
import copy
import datetime
import re
import time

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle
from urllib.error import URLError
from urllib.request import urlopen

CURRENT_DATE = datetime.datetime.date(datetime.datetime.now())
BASE_URL = "https://www.basketball-reference.com/"
MAX_TRIES = 5


def get_soup(url):
    # this is the HTML from the given URL
    html = None
    tries = 0
    while not html and tries < MAX_TRIES:
        try:
            html = urlopen(url, timeout=20)
        except:
            print("try url again")
            time.sleep(tries**2)  # exponential back off
            tries += 1

    # if we've tried 10 times let's just skip this URL
    if tries == MAX_TRIES:
        return None

    soup = None
    tries = 0
    while not soup and tries < MAX_TRIES:
        try:
            soup = BeautifulSoup(html, "html.parser")
        except:
            print("try soup again")
            time.sleep(tries**2)
            tries += 1

    if tries == MAX_TRIES:
        return None

    return soup


def get_box_score_links(soup):
    """Get all the links to the individual game stats from a soup object."""
    all_results = soup.find_all("a", href=re.compile("boxscores"))
    box_score_links = []
    for result in all_results:
        if result.text == "Final":
            box_score_links.append(result.attrs["href"])

    if len(box_score_links) < 1:
        raise IndexError("No games today")

    return box_score_links


def get_season_box_score_links(soup):
    """Get all the links to the individual game stats from a soup object."""
    month_links = get_month_links(soup)
    urls = [BASE_URL + link for link in month_links]
    box_score_links = []
    for url in urls:
        soup = get_soup(url)
        box_cells = soup.find_all("td", attrs={"data-stat": "box_score_text"})
        for box_cell in box_cells:
            link = box_cell.find("a")
            if link:
                box_score_links.append(link["href"])

    return box_score_links


def get_month_links(soup):
    """Get all the months where we have games for a certain season."""
    div = soup.find_all("div", attrs={"class": "filter"})
    month_links = [part["href"] for part in div[0].find_all("a")]
    return month_links


def get_4factor_stat(soup, stat_name):
    """Function to get one of the 4 factor stats"""
    cells = soup.find_all("td", attrs={"data-stat": stat_name})
    return cells[0].contents[0], cells[1].contents[0]


def get_all_4factor_stats(soup):
    away_stats = []
    home_stats = []
    for stat_name in STAT_NAMES:
        stats = get_4factor_stat(soup, stat_name)
        away_stats.append(stats[0])
        home_stats.append(stats[1])

    return away_stats, home_stats


def get_id_from_url(url):
    start_indicator = "boxscores/"
    end_indicator = ".html"
    start_idx = url.index(start_indicator) + len(start_indicator)
    end_idx = url.index(end_indicator)
    return url[start_idx:end_idx]


def get_score(soup):
    result_string = soup.find_all(string=re.compile("Line Score Table"))
    score_soup = BeautifulSoup(result_string[0], "html.parser")
    final_scores = score_soup.find_all("strong")
    return final_scores[0].contents[0], final_scores[1].contents[0]


class FourFactorParser:
    def __init__(self):
        self.data = {}
        self.STAT_NAMES = ["pace", "efg_pct", "tov_pct", "orb_pct", "ft_rate", "off_rtg"]

    def get_all_seasons(self, start_year, end_year):
        """Get all the seasons inclusive of start_year and end_year."""
        t0 = time.time()
        for year in range(start_year, end_year + 1):
            self.data[str(year)] = {}
            self.build_season_data(year)
            self.save_data(year)
            print("Finished year {} in {} seconds total".format(year, time.time()-t0))

    def build_season_data(self, year):
        """Function to get a full season's worth of data."""
        url = BASE_URL + f"leagues/NBA_{year}_games.html"
        soup = get_soup(url)

        links = get_season_box_score_links(soup)
        full_links = [BASE_URL + link for link in links]
        i = 0
        for url in full_links:
            self.add_game_data(url, year)
            i += 1

    def build_day_data(self, date):
        url = (
            BASE_URL + f"boxscores/?month={date.month}&day={date.day}&year={date.year}"
        )
        soup = get_soup(url)
        if not soup:  # url didn't work
            return "Fail"

        box_score_links = get_box_score_links(soup)

        for link in box_score_links:
            url = BASE_URL + link
            self.add_game_data(url)

        return "Success"

    def add_game_data(self, url, year):
        """Get the data we need from a single game."""
        soup = get_soup(url)
        if not soup:
            return "Fail"

        four_factors_string = soup.find_all(string=re.compile("Four Factors"))
        four_factors_soup = BeautifulSoup(four_factors_string[1], "html.parser")
        team_strings = four_factors_soup.find_all("a")
        team_ids = [string.contents[0] for string in team_strings]

        four_factors_stats = get_all_4factor_stats(four_factors_soup)
        team_scores = get_score(soup)

        game_dict = {}
        for i, (team_id, team_score, four_factors) in enumerate(
            zip(team_ids, team_scores, four_factors_stats)
        ):
            # if it's the first team they're away, second team is home
            game_loc = "A" if i == 0 else "H"
            game_dict[team_id] = [game_loc, team_score] + four_factors

        game_id = get_id_from_url(url)
        self.data[str(year)][game_id] = game_dict

        return "Success"

    def save_data(self, year):
        with open(
            f"../data/{year}_FourFactors.p", "wb"
        ) as f:
            pickle.dump(self.data, f)

    def load_data(self, year):
        with open(
            f"../data/{year}_FourFactors.p", "wb"
        ) as f:
            data = pickle.load(self.data, f)

        return data

    def make_game_dataframe(self, years):
        """Make dataframes for all the games for all the years in the list."""
        team_columns = ["team", "score"] + self.STAT_NAMES
        team_columns_h = ["_h" + col for col in team_columns]
        team_columns_a = ["_a" + col for col in team_columns]
        columns = ["game_id",  "date"] + team_columns_h + team_columns_a
        for year in years:
            year_data = self.load_data(year)
            array_data = []
            for game, teams in year_data.items():
                date = pd.Timestamp(game[:8])  # first 8 digits correspond to date in YYYYMMDD format
                for team, stats in teams.items():
                    if stats[0] == "H":
                        team_stats_h = stats
                    elif stats[0] == "A":
                        team_stats_a = stats
                    else:
                        raise ValueError("team designated as {} not H or A, full game: {}".format(stats[0], teams))

                game_stats = np.array([game, date] + team_stats_h + team_stats_a)
                array_data.append(game_stats)

        return pd.DataFrame(data=np.array(array_data), columns=columns).set_index('game_id')

    def make_team_performance_dataframe(self, years):
        """Here we build a dataframe such that each team for each game gets a row."""
        game_df = self.make_game_dataframe(years)

        # take the same columns as before except instead of home and away now we have self and opponent
        team_columns = ["team", "score"] + self.STAT_NAMES
        team_columns_self = ["_self" + col for col in team_columns]
        team_columns_opp = ["_opp" + col for col in team_columns]
        columns = ["game_id",  "date"] + team_columns_self + team_columns_opp

        # for the first half of the dataframe we can just change the column names
        result_df = copy.deepcopy(game_df)
        result_df.columns = columns

        """Now flip the stat columns and append. 
           We can do this by just renaming the columns and they should automatically rearrange on append"""
        temp_df = copy.deepcopy(result_df)
        temp_df.columns = ["game_id",  "date"] + team_columns_opp + team_columns_self

        result_df = result_df.append(temp_df)
        return result_df


if __name__ == "__main__":

    # this is the HTML from the given URL
    ffp = FourFactorParser()

    ffp.get_all_seasons(start_year=2009, end_year=2020)
