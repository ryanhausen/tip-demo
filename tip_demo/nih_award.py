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
    def from_nih_api(data: dict) -> "NihAward":
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
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NihAward):
            raise NotImplemented("Cannot compare NihAward to other type")

        return self.appl_id == other.appl_id

    def __hash__(self) -> int:
        return hash(self.appl_id)

