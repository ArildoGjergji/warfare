from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Tuple, Dict, ClassVar

class UnitType(Enum):
    INFANTRY = "infantry"
    ARMOR = "armor"
    ARTILLERY = "artillery"
    AIR_SUPPORT = "air_support"
    RECON = "recon"

class EngagementResult(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    STALEMATE = "stalemate"

@dataclass
class Unit:
    id: int
    unit_type: UnitType
    strength: float
    position: Tuple[float, float]
    speed: float
    detection_range: float
    attack_range: float
    attack_power: float
    defense: float
    
    _type_multipliers: ClassVar[Dict[Tuple[UnitType, UnitType], float]] = {
        (UnitType.INFANTRY, UnitType.ARMOR): 0.5,
        (UnitType.ARMOR, UnitType.INFANTRY): 1.5,
        (UnitType.ARTILLERY, UnitType.INFANTRY): 2.0,
        (UnitType.AIR_SUPPORT, UnitType.ARMOR): 1.8,
        (UnitType.RECON, UnitType.INFANTRY): 0.3,
    }

@dataclass
class Engagement:
    attacker_id: int
    defender_id: int
    result: EngagementResult
    attacker_loss: float
    defender_loss: float
    timestamp: float = field(default_factory=time.time)