import logging
import random
from collections import defaultdict
from simulation import WarfareSimulation
from models import UnitType

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('warfare_simulation.log', mode='a'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    simulation = WarfareSimulation(map_size=(800.0, 600.0))
    
    # Create forces
    logger.info("Creating forces...")
    for side in [0, 200], [600, 800]:
        for _ in range(10):
            simulation.create_unit(
                random.choice(list(UnitType)),
                (random.uniform(side[0], side[1]), random.uniform(0, 600))
            )
    
    # Run simulation
    logger.info("Starting simulation...")
    total_stats = defaultdict(int)
    
    for step in range(50):
        logger.info(f"Step {step + 1}")
        step_stats = simulation.run_simulation_step()
        
        for key, value in step_stats.items():
            total_stats[key] += value
        
        if len(simulation.units) <= 1:
            logger.info("Simulation complete")
            break
    
    # Summary
    logger.info("=== Summary ===")
    logger.info(f"Engagements: {total_stats['engagements']}")
    logger.info(f"Units destroyed: {total_stats['units_destroyed']}")
    logger.info(f"Final units: {len(simulation.units)}")
    logger.info(f"Total engagements: {len(simulation.engagements)}")

if __name__ == "__main__":
    main()