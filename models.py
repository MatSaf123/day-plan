import pydantic


class DayPlanEntry(pydantic.BaseModel):
    """One entry (line) extracted from the day plan file."""
    name: str
    start_time: str  # Hour and minutes, HH:MM
    end_time: str  # Hour and minutes, HH:MM
    comment: str | None = None
