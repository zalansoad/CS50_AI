corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damping_factor = 0.85

pages = []
for html in corpus:
        for link in corpus[html]:
            if link not in pages:
                pages.append(link)
    

default_odds = (1 - damping_factor) / len(corpus)
rand_jump = damping_factor / len(pages)

result_dict = {}
keys_list = list(corpus.keys())
print(keys_list)

for key in keys_list:
    if key in pages:
          result_dict[key] = rand_jump + default_odds
    else:
         result_dict[key] = default_odds
     
print (result_dict)