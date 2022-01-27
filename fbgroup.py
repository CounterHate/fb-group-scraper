from dataclasses import dataclass


@dataclass
class Group:
    group_id: str
    group_name: str
    private: bool
    email: str
    password: str
