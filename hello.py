from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from bs4 import BeautifulSoup
import requests

class CricketScore:
    def __init__(self, rootWindow):
        self.rootWindow = rootWindow
        self.rootWindow.title('LIVE CRICKET SCORE')
        self.rootWindow.geometry('800x500')

        try:
            self.bg = ImageTk.PhotoImage(file="C:\\Users\\Admin\\New folder\\project.py\\oops.py\\crickfev.png")
            bg = Label(self.rootWindow, image=self.bg)
            bg.place(x=0, y=0)
        except:
            print("Background image not found. Continuing without background.")

        self.label = Label(self.rootWindow, text='Live Matches',
                           font=("times new roman", 30), compound='center')
        self.label.pack(padx=100, pady=20)

        self.var = StringVar()
        self.matches = self.match_details()

    def match_details(self):
        details = self.scrap()
        live_match = {}

        for detail in details:
            live_team_details = {}
            summary = self.match_summary(detail)
            if summary is not None:
                match_header = self.match_header(detail).text.strip() if self.match_header(detail) else "No Header"
                teams = self.teams_name(detail)
                live_team_details["summary"] = summary.text.strip()
                live_team_details["teams"] = teams
                live_match[match_header] = live_team_details
                print(f"{match_header}: {teams} - {summary.text.strip()}")

        return live_match

    def teams_name(self, detail):
        teams = []
        team1 = detail.find("div", class_="cb-hmscg-bat-txt")
        team2 = detail.find("div", class_="cb-hmscg-bwl-txt")
        if team1:
            teams.append(team1.text.strip())
        if team2:
            teams.append(team2.text.strip())
        return teams

    def match_summary(self, detail):
        return detail.find("div", class_="cb-match-crd-state")

    def match_header(self, detail):
        return detail.find("div", class_="cb-match-crd-hdr")

    def scrap(self):
        URL = "https://www.cricbuzz.com/api//cricket-match//live-scores"
        headers={
            "User-Agent":'Mozilla/5.0'
        }
        #headers={
            #'User-Agent': "Mozilla/5.0"
        #}
        try:
            page = requests.get(URL,headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            matches = soup.find_all("div",class_="cb-mtch-1st cb-col cb-col-100 cb-tms-itm")
            if matches:
                print(f"Found{len(matches)}live matches.")
                return matches
            else:
                print("No match data found on page.")
                return []
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

def main():
    rootWindow = Tk()
    app = CricketScore(rootWindow)
    rootWindow.mainloop()

if __name__ == '__main__':
    main()
