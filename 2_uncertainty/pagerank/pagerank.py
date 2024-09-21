import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if not corpus[page]:
        odds = 1/len(corpus)
        result_dict = {}

        for key in corpus:
            result_dict[key] = odds

        return result_dict
    
    else:
        pages = corpus[page]
        
        default_odds = (1 - damping_factor) / len(corpus)
        rand_jump = damping_factor / len(pages)

        result_dict = {}

        for key in corpus:
            if key in pages:
                result_dict[key] = rand_jump + default_odds
            else:
                result_dict[key] = default_odds

        return result_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    count_dict = {}
    current = random.choice(list(corpus.keys()))
    count_dict[current] = 1

    
    for i in range(n):
        prob_distr = transition_model(corpus, current, damping_factor)
        keys = list(prob_distr.keys())
        values = []
        for prob in prob_distr:
            values.append(prob_distr[prob])

        current = random.choices(keys, values)[0]
        
        if current not in count_dict:
            count_dict[current] = 1
        else:
            count_dict[current] = count_dict[current] + 1
    
    result_dict = count_dict
    for key in result_dict:
        result_dict[key] = result_dict[key] / n

    return result_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    N = len(corpus)
    ranked_pages = {key: 1 / N for key in corpus}
        
    final_rank = {key: value for key, value in ranked_pages.items()}
    rank_flag = True

    while rank_flag:

        for p in corpus:
            #how many pages link to key
            i = []
            for page in corpus:
                if not corpus[page]: #A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                    i.append(page)
                elif p in corpus[page]:
                    i.append(page) #key oldalra enny oldal mutat
                    


            # Vegyük minden olyan i oldalt, amelyik linkel a p oldalra.
            # Minden ilyen i oldalhoz számoljuk ki Pr(i)/Numlinks(i)
            # Adjuk össze az összes ilyen i oldalra kiszámított ertekeket.
            # égül az eredményt szorozzuk meg a d értékkel
            
            sum_i = 0
            for page in i:
                if not corpus[page]:
                    NumLinks = len(corpus) #A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                    sum_i += ranked_pages[page]/NumLinks
                else:
                    NumLinks = len(corpus[page]) # hany link van az i oldalon
                    sum_i += ranked_pages[page]/NumLinks

            previous_rank = ranked_pages[p]
            ranked_pages[p] = (1 - damping_factor)/N + damping_factor * sum_i
        
        num_ok = 0
        for key in ranked_pages:
            if final_rank[key] - ranked_pages[key] < 0.001:
                num_ok += 1
                #flag valtoztatas
        if num_ok == len(ranked_pages):
            rank_flag = False
        
        final_rank = {key: value for key, value in ranked_pages.items()} #setting final rank to current calculated ranks

    return final_rank

if __name__ == "__main__":
    main()
