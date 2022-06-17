
import requests, csv
from bs4 import BeautifulSoup
from datetime import datetime

class Steam:

    def __init__(self):
        self.url = 'https://store.steampowered.com/stats/'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def find_player_numbers(self) -> list:
        self.viewers = self.soup.select('span', class_='statsTopHi')
        return self.viewers

    def find_game_titles(self) -> list:
        self.titles = self.soup.select('td a')
        return self.titles

class Csv:

    def __init__(self):
        self.csv = csv

    def get_time(self) -> tuple:
        time = datetime.now()

        if len(str(time.month)) == 1:
            month = '0' + str(time.month)
        else:
            month = time.month

        if len(str(time.day)) == 1:
            day = '0' + str(time.day)
        else:
            day = time.day

        date = str(time.year) + '-' + str(month) + '-' + str(day)
        time = str(time.hour) + ':' + str(time.minute)

        return date, time

    def write_files(self, date, time, name, current, peak) -> None:
        output = open('output.csv', 'a', newline='')
        output_DictWriter = self.csv.DictWriter(output,
                                                ['Game_name',
                                                'Current_players',
                                                'Peak_players',
                                                'Date',
                                                'Time'])

        #self.output_DictWriter.writeheader()
        for (game, c_players, p_players) in zip(name, current, peak):
            output_DictWriter.writerow({'Game_name' : game,
                                        'Current_players' : c_players,
                                        'Peak_players' : p_players,
                                        'Date' : date,
                                        'Time' : time})
        output.close()

def get_current_players(c_viewers) -> list:

    current_players = []
    index = 1
    for item in c_viewers:
        if index % 2 != 0:
            current_players.append(item.text)
        index +=1

    return current_players

def get_peak_today(peak) -> list:

    peak_players = []
    index = 1
    for item in peak:
        if index % 2 == 0:
            peak_players.append(item.text)
        index +=1

    return peak_players

def get_game_titles(games) -> list:

    game_titles = []
    for game in games:
        game_titles.append(game.text)

    return game_titles

def display_games(names, current, peak) -> None:
    for (game, player_numbers, peak_players) in zip(names, current, peak):
        print(f'Game: {game}  ...Current Players: {player_numbers} ...Peak Players: {peak_players}')

def main():
    steam = Steam()
    csv = Csv()
    all_numbers = steam.find_player_numbers()
    all_titles = steam.find_game_titles()
    current_players = get_current_players(all_numbers[25:44])
    peak_players =  get_peak_today(all_numbers[25:45])
    game_titles = get_game_titles(all_titles[:10])
    date_time = csv.get_time()
    csv.write_files(date_time[0], date_time[1], game_titles, current_players, peak_players)
    display_games(game_titles, current_players, peak_players)

if __name__ == '__main__':
    main()
