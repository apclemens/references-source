import pickle

data = pickle.load(open('data.p', 'rb'))

lowest_year = 2000
highest_year = 0
highest_value = 0
for year in list(data.keys()):
    for ref in data[year]:
        if ref < lowest_year:
            lowest_year = ref
        if ref > highest_year:
            highest_year = ref
        if data[year][ref] > highest_value:
            highest_value = data[year][ref]


graph_width = 500
graph_margin = 0
a = (graph_width - graph_margin) / (highest_year + 1 - lowest_year)
b = - a * lowest_year

