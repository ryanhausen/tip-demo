import json


def main():
    ml_authors = []

    with open("pis-2019.json", "r") as f, open("pis-2020.json", "r") as g:
        ml_authors.extend(list(map(lambda x: x["profile_id"], json.load(f))))

        ml_authors.extend(list(map(lambda x: x["profile_id"], json.load(g))))

    ml_authors = list(set(ml_authors))

    with open("awards-2018.json", "r") as f:
        all_awards = json.load(f)

    relevant_awards = list(
        filter(
            lambda x: any(pi in ml_authors for pi in x["principal_investigators"]),
            all_awards,
        )
    )

    print(f"{len(relevant_awards)} relevant awards of {len(all_awards)} total awards")

    with open("awards-2018-candidate.json", "w") as f:
        json.dump(relevant_awards, f, indent=2)


if __name__ == "__main__":
    main()
