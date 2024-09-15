corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damping_factor = 0.85
if not corpus[page]:
    odds = 1/len(corpus)
    result_dict = {}

    for key in corpus:
        result_dict[key] = odds

pages = corpus[page]

default_odds = (1 - damping_factor) / len(corpus)
rand_jump = damping_factor / len(pages)

result_dict = {}


for key in corpus:
    if key in pages:
          result_dict[key] = rand_jump + default_odds
    else:
         result_dict[key] = default_odds
     
print (result_dict)