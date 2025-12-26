import logging
import random
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from models import Unit, UnitType, Engagement, EngagementResult

logger = logging.getLogger(__name__)

class WarfareSimulation:
    def __init__(self, map_size: Tuple[float, float] = (1000.0, 1000.0)):
        self.map_size = map_size
        self.units: Dict[int, Unit] = {}
        self.engagements: List[Engagement] = []
        self.unit_counter = 0
    
    def create_unit(self, unit_type: UnitType, position: Tuple[float, float]) -> Unit:
        self.unit_counter += 1
        unit = Unit(
            id=self.unit_counter,
            unit_type=unit_type,
            strength=1.0,
            position=position,
            speed=random.uniform(0.5, 2.0),
            detection_range=random.uniform(50.0, 200.0),
            attack_range=random.uniform(20.0, 150.0),
            attack_power=random.uniform(0.5, 1.5),
            defense=random.uniform(0.3, 0.9)
        )
        self.units[unit.id] = unit
        logger.info(f"Created {unit_type.value} unit {unit.id} at {position}")
        return unit
    
    def _find_nearby_enemies(self, unit_id: int, max_distance: float) -> List[int]:
        if not self.units or unit_id not in self.units:
            return []
        
        unit = self.units[unit_id]
        positions = np.array([u.position for u in self.units.values() if u.id != unit_id])
        unit_ids = [u.id for u in self.units.values() if u.id != unit_id]
        
        if len(positions) == 0:
            return []
        
        distances = np.sqrt(np.sum((positions - np.array(unit.position))**2, axis=1))
        return [unit_ids[i] for i, d in enumerate(distances) if d <= max_distance]
    
    def _simulate_engagement(self, attacker_id: int, defender_id: int) -> EngagementResult:
        attacker = self.units[attacker_id]
        defender = self.units[defender_id]
        
        type_multiplier = Unit._type_multipliers.get(
            (attacker.unit_type, defender.unit_type), 1.0
        )
        
        effective_attack = attacker.attack_power * type_multiplier * attacker.strength
        effective_defense = defender.defense * defender.strength
        
        random_factor = random.uniform(0.8, 1.2)
        attacker_damage = effective_defense * random_factor * 0.1
        defender_damage = effective_attack * random_factor * 0.15
        
        attacker.strength = max(0.0, attacker.strength - attacker_damage)
        defender.strength = max(0.0, defender.strength - defender_damage)
        
        if defender.strength <= 0:
            result = EngagementResult.VICTORY
        elif attacker.strength <= 0:
            result = EngagementResult.DEFEAT
        else:
            result = EngagementResult.STALEMATE
        
        self.engagements.append(Engagement(
            attacker_id=attacker_id,
            defender_id=defender_id,
            result=result,
            attacker_loss=attacker_damage,
            defender_loss=defender_damage
        ))
        
        if attacker.strength <= 0:
            del self.units[attacker_id]
        if defender.strength <= 0:
            del self.units[defender_id]
        
        return result
    
    def _move_unit(self, unit_id: int) -> None:
        unit = self.units[unit_id]
        target = (
            random.uniform(0, self.map_size[0]),
            random.uniform(0, self.map_size[1])
        )
        
        dx, dy = target[0] - unit.position[0], target[1] - unit.position[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance <= unit.speed:
            unit.position = target
        else:
            unit.position = (
                unit.position[0] + (dx / distance) * unit.speed,
                unit.position[1] + (dy / distance) * unit.speed
            )
    
    def run_simulation_step(self) -> Dict[str, int]:
        stats = defaultdict(int)
        stats["units_active"] = len(self.units)
        
        unit_ids = list(self.units.keys())
        random.shuffle(unit_ids)
        
        for unit_id in unit_ids:
            if unit_id not in self.units:
                continue
                
            unit = self.units[unit_id]
            enemies = self._find_nearby_enemies(unit_id, unit.detection_range)
            
            for enemy_id in enemies[:2]:
                if enemy_id in self.units:
                    result = self._simulate_engagement(unit_id, enemy_id)
                    stats["engagements"] += 1
                    if result != EngagementResult.STALEMATE:
                        stats["units_destroyed"] += 1
        
        for unit_id in self.units:
            if random.random() > 0.7:
                self._move_unit(unit_id)
        
        return stats