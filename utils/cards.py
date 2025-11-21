import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone,timedelta
from typing import Dict
from utils.deck import load_deck, save_deck
import heapq
import itertools


counter = itertools.count()
steps = {1: timedelta(minutes=1),
         2: timedelta(minutes=6),
         3: timedelta(minutes=10)}

def _now() -> datetime:
    return datetime.now(timezone.utc)

def human_date(iso_ts: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_ts)
    except ValueError:
        return iso_ts
    return dt.astimezone().strftime("%d-%m-%Y %H:%M:%S")

@dataclass
class Card:
    id : str
    front : str
    back : str
    interval : int = 1
    ease_factor : float = 2.5
    step : int = 1
    due : str = _now().isoformat()
    first_time : bool = True

    @classmethod
    def from_dict(self, raw:Dict[str, object]) -> "Card":
        return self(**raw)
    
    def to_dict(self) -> Dict[str, object]:
        return asdict(self)
    
    @classmethod
    def new(self, front: str, back: str) -> "Card":
        return self(
            id = str(uuid.uuid4()),
            front = front,
            back = back,
            due = _now().isoformat(),
            first_time = True
        )
    


#card scheduling algorithm modified SM-2
def update_schedule(card: Card, quality: int) -> None:
    now = _now()

    if quality <0 or quality > 3:
        raise ValueError("Quality must be between 0 and 3")
    else:
        if (quality == 0 or card.step < 3) and quality < 3:
            learning_steps(card, quality)
        else:
            card.step = 4
            due = now + timedelta(days=card.interval)
            card.due = due.isoformat()
            if quality == 1:
                card.ease_factor -= 0.15
                card.interval = card.interval * 1.2
            elif quality == 2:
                card.interval = card.interval * card.ease_factor
            else:
                card.ease_factor += 0.15
                card.interval = card.interval * card.ease_factor * 1.3
            card.ease_factor = max(1.3, card.ease_factor)
            card.interval = round(card.interval)
    card.first_time = False

#learning session & lapses
def learning_steps(card: Card, quality: int) -> None:

    now = _now()
    if card.step < len(steps):
        if quality < 0 or quality > 2:
            raise ValueError("qualitty must be between 0 to 3")
        if quality == 0:
            card.step = 1
        elif quality == 1:
            card.step += 1
        elif quality == 2:
            card.step += 2
        elif quality == 3:
            card.step = 3
        card.interval = 1
    step = min(card.step, 3)
    due = now + steps[step]
    card.due = due.isoformat()
    card.first_time = False

#add new card into decks
def add_card(front, back, deck_name: str):
    deck = load_deck(deck_name)
    card = Card.new(front = front, back = back)
    deck.append(card.to_dict())
    save_deck(deck_name, deck)

#start studying session
def card_queue(deck_name: str, new_limit: int = 9999, due_limit: int = 9999):
    cards_raw = load_deck(deck_name)
    cards = [Card.from_dict(c) for c in cards_raw]
    now = _now()
    
    new_cards = []
    due_cards = []

    session_cards = []
    for c in cards:
        due_dt = datetime.fromisoformat(c.due)
        if c.step == 1 and c.first_time == True:
            new_cards.append((due_dt, c))
        elif due_dt <= now and c.step >= 4:
            due_cards.append((due_dt, c))
        elif c.step < 4:
            heapq.heappush(session_cards,(due_dt, next(counter), c))

    if new_limit is not None:
        if new_limit > 0:
            new_cards = new_cards[:new_limit]
        else: new_cards = due_cards[:0]
    if due_limit is not None:
        if due_limit > 0:
            due_cards = due_cards[:due_limit]
        else: due_cards = due_cards[:0]
    for due_dt, c in new_cards + due_cards:
        heapq.heappush(session_cards,(due_dt, next(counter), c))

    return session_cards

def card_status(queue):
    new_card = sum(1 for c in queue if getattr(c[2], "first_time") == True)
    review = sum(1 for c in queue if getattr(c[2], "first_time") == False and getattr(c[2], "step")<= 4 )
    due = sum(1 for c in queue if getattr(c[2], "first_time") == False and getattr(c[2], "step")>= 4
              and datetime.isoformat(getattr(c[2], "due"))<= datetime.now(timezone.utc))
    y = [new_card, review, due]
    return y
        
def reset_due(deck_name: str):
    raw_cards = load_deck(deck_name)
    cards = [Card.from_dict(c) for c in raw_cards]
    now = _now()
    for c in cards:
        c.due = now.isoformat()
        c.first_time = True
        c.interval = 1
        c.step = 1
        c.ease_factor = 2.5
    cards = [Card.to_dict(c) for c in cards]
    save_deck(deck_name, cards)
