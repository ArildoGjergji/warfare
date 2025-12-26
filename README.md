# Modern Warfare Simulation

A minimal, efficient Python simulation for modern warfare scenarios featuring unit combat, movement, and engagement tracking.

## File Descriptions

### `models.py` - Data Models and Types

Contains all data structures and type definitions used throughout the simulation:

**Key Components:**
- `UnitType` (Enum): Military unit classifications (Infantry, Armor, Artillery, Air Support, Recon)
- `EngagementResult` (Enum): Possible battle outcomes (Victory, Defeat, Stalemate)
- `Unit` (Dataclass): Represents a military unit with attributes:
  - `id`: Unique identifier
  - `unit_type`: Type of unit
  - `strength`: Combat effectiveness (0.0 to 1.0)
  - `position`: (x, y) coordinates on map
  - `speed`: Movement capability
  - `detection_range`: How far the unit can see enemies
  - `attack_range`: How far the unit can engage
  - `attack_power`: Offensive capability
  - `defense`: Defensive capability
  - `_type_multipliers`: Class variable defining rock-paper-scissors style advantages
- `Engagement` (Dataclass): Record of combat encounters with timestamps

**Purpose:** Provides clean, typed data structures that ensure type safety and reduce errors. Using dataclasses minimizes boilerplate code while maintaining clarity.

### `simulation.py` - Core Simulation Engine

Contains the main simulation logic and algorithms:

**Key Components:**
- `WarfareSimulation` class: Main controller with methods:
  - `__init__()`: Initializes simulation with map size
  - `create_unit()`: Generates new units with randomized attributes
  - `_find_nearby_enemies()`: Efficient vectorized enemy detection using NumPy
  - `_simulate_engagement()`: Resolves combat with type advantages and random factors
  - `_move_unit()`: Handles unit movement towards random targets
  - `run_simulation_step()`: Executes one complete simulation cycle

**Performance Features:**
- **Vectorized operations**: Uses NumPy for efficient distance calculations
- **O(1) lookups**: Dictionary-based unit storage
- **Batch processing**: Processes multiple engagements per step
- **Memory efficient**: Removes destroyed units immediately

**Combat Mechanics:**
- Type advantages (e.g., Armor beats Infantry)
- Strength-based combat resolution
- Random factors for realism
- Progressive unit weakening

### `main.py` - Execution and Logging

Manages simulation setup, execution, and logging:

**Key Functions:**
- `setup_logging()`: Configures dual logging to file and console
- `main()`: Primary execution flow:
  1. Initializes simulation with 800x600 map
  2. Creates two opposing forces (10 units each)
  3. Runs simulation for up to 50 steps
  4. Tracks and reports statistics
  5. Ends when one side is eliminated

**Logging Configuration:**
- **File logging**: `warfare_simulation.log` (append mode)
- **Console logging**: Real-time output
- **Format**: Timestamp - Level - Message
- **Level**: INFO (configurable)

## Installation and Usage

Prerequisites: numpy

Usage: python main.py
### Prerequisites
```bash
pip install numpy
