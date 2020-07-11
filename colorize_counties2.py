import csv
from bs4  import BeautifulSoup

reader = csv.reader(open('unemployment-aug2010.txt', 'r'), delimiter=',')
svg = open('USA_Counties_with_FIPS_and_names.svg', 'r').read()

unemployment = {}
rates_only = []
past_header = False
min_value = 100
max_value = 0
for row in reader:
    if not past_header:
        past_header = True
        continue

    try:
        full_fips = 'FIPS_' + row[1] + row[2]
        rate = float(row[5].strip())
        unemployment[full_fips] = rate
        rates_only.append(rate)
    except:
        pass

# Quartiles
rates_only.sort()
q1_index = int(0.25*len(rates_only))
q1 = rates_only[q1_index]

q2_index = int(0.5*len(rates_only))
q2 = rates_only[q2_index]

q3_index = int(0.75 * len(rates_only))
q3 = rates_only[q3_index]

soup = BeautifulSoup(svg, 'xml')
paths = soup.findAll('path')

colors = ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#6a51a3']
path_style = 'font-size:12px;fill-style-rule:nonzero;stroke:#fffff;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-disharray:none;stroke-linecap:butt;marker-start:nonr;stroke-linejoin:bevel;fill:'

for p in paths:
    rate = 0
    color_class = 0
    if p['id'] not in ['State_Lines', 'separator']:
        try:
            rate = unemployment[p['id']]
        except:
            continue
        if rate > q3:
            color_class = 3
        elif rate > q2:
            color_class = 2
        elif rate > q1:
            color_class = 1
        else:
            color_class = 0

        color = colors[color_class]
        p['style'] = path_style + color

print(soup.prettify())
