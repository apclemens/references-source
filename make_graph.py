from PIL import Image, ImageDraw
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

graph_height = 1500
graph_width = 1500
graph_margin = 10

pic_height = graph_height + 2*graph_margin
pic_width = graph_width + 2*graph_margin

im = Image.new("RGB", (pic_width, pic_height), 'white')
draw = ImageDraw.Draw(im)

draw.line((graph_margin, graph_margin, graph_margin, graph_margin+graph_height), fill=128)
draw.line((graph_margin, graph_margin+graph_height, graph_margin+graph_width, graph_margin+graph_height), fill=128)

def year_to_coord(year):
    a = (graph_width - graph_margin) / (max(data.keys()) + 1 - lowest_year)
    b = graph_margin - a * lowest_year
    return a*year + b

def years_to_rect(year, ref):
    return [
        year_to_coord(year),
        graph_height - year_to_coord(ref+1),
        year_to_coord(year+1),
        graph_height - year_to_coord(ref)
    ]

# loop years from lowest_year to max(data.keys())
for year in range(lowest_year, max(data.keys()) + 1):
    if year not in list(data.keys()): continue
    for ref in list(data[year].keys()):
        shade = int(255.0*data[year][ref]/highest_value)
        draw.rectangle(years_to_rect(year, ref), fill=(shade, shade, shade))

im.save('graph.png', "PNG")
