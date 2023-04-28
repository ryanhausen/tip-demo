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


def download_nih_data(year:int):
    search_criteria = dict(
        spending_categories=dict(
            values=[4372], # spending category 4372 is for machine learning and artificial intelligence
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
        limit=10,
        offset=0,
    )

    pis = []
    awards = []

    for result in results:
        results_pis = list(map(
            NihPi.from_nih_api,
            result["principal_investigators"]
        ))

        results_award = NihAward.from_nih_api(result)

        pis.extend(results_pis)
        awards.append(results_award)

    pis = list(set(pis))

    return results



def main():

    results = download_nih_data(2019)

    print(results)



if __name__=="__main__":
    main()