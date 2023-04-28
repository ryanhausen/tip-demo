import dataclasses as dc
from typing import List

@dc.dataclass
class NihAward:
    appl_id: int
    project_num: str
    project_title: str
    project_deatil_url: str
    principal_investigators: List[int]

    @staticmethod
    def from_nih_api(data: dict, ) -> "NihAward":
        return NihAward(
            appl_id=data["appl_id"],
            project_num=data["project_num"],
            project_title=data["project_title"],
            project_deatil_url=data["project_detail_url"],
            principal_investigators=list(map(
                lambda pi: pi["profile_id"],
                data["principal_investigators"],
            )),
        )

