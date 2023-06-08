import os

from itertools import product
from fundNSF import FundNSF



def main():
    nsf = FundNSF()


    mapping = " \"{}\":\"{}\" "

    years_topics = product(
        range(2010, 2022),
        ["Machine Learning", "Artificial Intelligence"]
    )

    for year, topic in years_topics:
        if os.path.exists(f"{topic}-{year}.json"):
            continue

        print(f"Working on {year}-{topic}")
        nsf.set_params(
            startDateStart = f"01/01/{year}",
            startDateEnd = f"12/31/{year}",
        )
        nsf.set_fields(
            pdPIName=True,
            perfAddress=True,
            piEmail=True,
            startDate=True,
            expDate=True,
            fundProgramName=True,
            fundAgencyCode=True,
            awardAgencyCode=True,
        )

        result = nsf.keyword_search(topic)
        with open(f"{topic}-{year}.json", "w") as f:
            for item in result:
                string_item = "{ " + ",".join(
                    [mapping.format(*i) for i in item.items()]
                ) + " } \n"
                f.write(string_item)


if __name__ == "__main__":
    main()