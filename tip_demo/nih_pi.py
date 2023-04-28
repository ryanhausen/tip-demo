
import dataclasses as dc
from typing import Optional

@dc.dataclass
class NihPi:
    profile_id: int
    first_name: str
    middle_name: str
    last_name: str
    email: Optional[str] = None

    @staticmethod
    def from_nih_api(data: dict) -> "NihPi":
        return NihPi(
            profile_id=data["profile_id"],
            first_name=data["first_name"],
            middle_name=data["middle_name"],
            last_name=data["last_name"],
            email=data["email"],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NihPi):
            raise NotImplemented("Cannot compare NihPi to other type")

        return self.profile_id == other.profile_id

    def __hash__(self) -> int:
        return hash(self.profile_id)