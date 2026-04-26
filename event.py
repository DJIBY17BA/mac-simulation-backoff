from dataclasses import dataclass

ARRIVE = "ARRIVE"
TRY = "TRY"
FINISH = "FINISH"

@dataclass(order=True)
class Event:
    time: float
    event_type: str
    station_id: int