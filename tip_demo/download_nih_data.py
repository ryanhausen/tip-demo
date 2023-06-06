import dataclasses as dc
from itertools import count
import json
from typing import List, Tuple

from pynih import apis

from nih_award import NihAward
from nih_pi import NihPi

INCLUDE_FIELDS = [
    "ApplId",
    "ProjectTitle",
    "OrgName",
    "ContactPiName",
    "PrincipalInvestigators",
    "ProjectNum",
    "ProjectDetailUrl",
]


def download_nih_data(
    year: int,
    spending_categories: List[int] = [4372],
    limit: int = 500,
    offset: int = 0,
) -> Tuple[List[NihAward], List[NihPi]]:
    search_criteria = dict(
        spending_categories=dict(
            values=spending_categories,  # spending category 4372 is for machine learning and artificial intelligence
            match_all=False,
        ),
        project_start_date=dict(
            from_date=f"{year}-01-01",
            to_date=f"{year}-12-31",
        ),
    )

    results = apis.query_project_api(
        include_fields=INCLUDE_FIELDS,
        search_criteria=search_criteria,
        limit=limit,
        offset=offset,
    )

    pis = []
    awards = []

    for result in results:
        results_pis = list(map(NihPi.from_nih_api, result["principal_investigators"]))

        results_award = NihAward.from_nih_api(result)

        pis.extend(results_pis)
        awards.append(results_award)

    pis = list(set(pis))
    awards = list(set(awards))

    return awards, pis


def main():

    years = [2019, 2020, 2021, 2022]

    for year in years:
        spending_categories = [4372] if year > 2018 else None
        limit = 500
        awards, pis = [], []
        for i in count(0):
            tmp_awards, tmp_pis = download_nih_data(
                year,
                spending_categories=spending_categories,
                limit=limit,
                offset=i * limit,
            )

            print(f"Downloaded {len(tmp_awards)} awards for {year}")
            awards.extend(tmp_awards)
            pis.extend(tmp_pis)

            if len(tmp_awards) < limit or (i + 1) * limit > 14_999:
                break

        for item, name in [(awards, "awards"), (pis, "pis")]:
            print(f"{len(item)} {name} for {year}")
            with open(f"{name}-{year}.json", "w") as f:
                json.dump(list(map(dc.asdict, item)), f, indent=2)


if __name__ == "__main__":
    main()
