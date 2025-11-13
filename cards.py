import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone,timedelta
from typing import Dict

def _now() -> datetime:
    return datetime.now(timezone.utc)

def human_date(iso_ts: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_ts)
    except ValueError:
        return iso_ts
    return dt.timezone().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Card:
    id : str
    front : str
    back : str
    interval : int = 1
    ease_factor : float = 2.5
    step : int = 1
    due : str = _now().isoformat()

    @dataclass
    def from_dict(self, raw:Dict[str, object]) -> "Card":
        return self(**raw)
    
    def to_dict(self) -> Dict[str, object]:
        return asdict(self)
    
    @classmethod
    def new(self, front: str, back: str) -> "Card":
        return self(
            id = str(uuid.uuid4()),
            front = front,
            back = back
        )
    
#card scheduling algorithm modified SM-2
def update_schedule(card: Card, quality: int) -> None:
    today = _now()
    if quality <0 or quality > 3:
        raise ValueError("Quality must be between 0 and 3")
    if card.repetitions == 0:
        card.interval = 1
    else:
        if quality == 0:
            learning_steps(card, quality)
        elif quality == 1:
            card.repetitions += 1
            card.ease_factor -= 0.15
            card.interval = card.interval * 1.2
        elif quality == 2:
            card.repetitions += 1
            card.interval = card.interval * card.ease_factor
        else:
            card.repetitions += 1
            card.ease_factor += 0.15
            card.interval = card.interval * card.ease_factor * 1.3
    card.ease_factor = max(1.3, card.ease_factor)
    card.interval = round(card.interval)

def learning_steps(card: Card, quality: int) -> None:
    now = _now
    next_show = now + datetime(minute=step)
    step = card.step()
    steps = {1: timedelta(minutes=1),
             1.5: timedelta(minutes=6),
             2: timedelta(minutes=10)}
    if step < len(steps):
        if quality < 0 or quality > 3:
            raise ValueError("qualitty must be between 0 to 3")
        if quality == 0:
            step = 1
        elif quality == 1:
            step += 0.5
        elif quality == 2:
            step += 1
        elif quality == 3:
            step = 3
        
        
    return 