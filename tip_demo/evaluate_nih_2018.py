import json
import matplotlib.pyplot as plt


from nih_award import NihAward
from nih_pi import NihPi

try:
    from tip_demo.algorithm_data_model import Author, Paper
except ImportError:
    from algorithm_data_model import Author, Paper

def main():

    ml_authors = []
    with open("pis-2019.json", "r") as f:
        ml_authors.extend(list(map(NihPi.from_nih_api, json.load(f))))

    ml_awards = []
    with open("awards-2019.json", "r") as f:
        ml_awards.extend(list(map(NihAward.from_nih_api, json.load(f))))

    ml_authors = list(set(ml_authors))

    for award in ml_awards:
        print(award.to_graph_object())




if __name__ == "__main__":
    main()


