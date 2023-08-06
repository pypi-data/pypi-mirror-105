
class Result:
    score: float
    selected_groups: list[int]
    matching_percent: float
    matching_users: list[str]
    matching_users_count: int
    extraneous_percent: float
    extraneous_users: list[str]
    extraneous_users_count: int
    unmatched_users: list[str]
    unmatched_users_count: int

    def __init__(self,
        score: float,
        selected_groups: list[int],
        matching_percent: float,
        matching_users: list[str],
        matching_users_count: int,
        extraneous_percent: float,
        extraneous_users: list[str],
        extraneous_users_count: int,
        unmatched_users: list[str],
        unmatched_users_count: int,
    ):
        self.score = score
        self.selected_groups = selected_groups
        self.matching_percent = matching_percent
        self.matching_users = matching_users
        self.matching_users_count = matching_users_count
        self.extraneous_percent = extraneous_percent
        self.extraneous_users = extraneous_users
        self.extraneous_users_count = extraneous_users_count
        self.unmatched_users = unmatched_users
        self.unmatched_users_count = unmatched_users_count

    def __str__(self) -> str:
        return f"""Score: {self.score}
Selected Groups: {self.selected_groups}
Matching Users Count: {self.matching_users_count}
Extraneous Users Count: {self.extraneous_users_count}
Unmatched Users Count: {self.unmatched_users_count}
Matching Percent: {self.matching_percent}
Extraneous Percent: {self.extraneous_percent}
"""

    def full_str(self):
        string = str(self)
        string = string + f"""Matching Users: {self.matching_users}
Unmatched Users: {self.unmatched_users}
Extraneous Users: {self.extraneous_users}
"""
        return string
