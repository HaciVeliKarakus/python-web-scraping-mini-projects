from tkinter import *
from tkinter import ttk
from tkinter.font import Font

import requests
from bs4 import BeautifulSoup

# main page url
url = "https://www.worldometers.info/coronavirus/"
html = requests.get(url)
# create soup
soup = BeautifulSoup(html.content, "html.parser")
# get table part of page
table = soup.find("table", id="main_table_countries_today")
# create a list for store table data
database = []
# get every tr element(one row = one country)
rows = table.find_all("tr")
# header for tree view columns
headers = ["#", "Country",
           "Total Cases", "New Cases",
           "Total Deaths", "New Deaths",
           "Total Recovered", "New Recovered",
           "Active Cases", "Serious,Critical",
           "Total Cases/1M pop", "Deaths/1M pop", "Total Tests", "Tests/1M pop",
           "Population",
           "Continent"]

for item in rows[9:]:
    row_data = item.text.split("\n")
    database.append(row_data[1:])

if __name__ == '__main__':
    # main window
    root = Tk()
    # root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
    # startup size
    root.geometry("1000x800")

    root.title("Coronavirus")

    # custom font
    font = Font(family="Arial", size=40, weight="bold")
    Label(root, text="COVID-19 CORONAVIRUS PANDEMIC", fg="green", font=font).pack()
    # create tree view for display like table
    tree_view = ttk.Treeview(root, columns=headers, show="headings")
    tree_view.pack(expand=YES, fill=BOTH)
    # add header to tree view
    for head in headers:
        tree_view.heading(head, text=head)
        tree_view.column(head, width=10)
    # add values to tree view line by line
    for data in database:
        tree_view.insert("", END, values=data)

    root.mainloop()
