import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Room:
    x: int
    y: int
    type: str = "normal"  # normal, entrance, exit, treasure, monster
    connections: List[Tuple[int, int]] = None
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []

class DungeonLSystem:
    def __init__(self):
        # L-System rules for dungeon generation
        self.rules = {
            'S': ['F[+F]F[-F]F'],  # Start rule - creates a basic branch
            'F': ['F', 'F[+F]', 'F[-F]', 'F[+F][-F]']  # Room placement rules
        }
        
        # Parameters for generation
        self.angle = 90  # Angle for turns (in degrees)
        self.step_size = 1
        self.current_pos = (0, 0)
        self.current_angle = 0
        self.rooms = {}  # Dictionary to store room positions
        
    def _apply_rules(self, sequence: str, iterations: int) -> str:
        """Apply L-System rules for given number of iterations"""
        for _ in range(iterations):
            new_sequence = ""
            for char in sequence:
                if char in self.rules:
                    new_sequence += random.choice(self.rules[char])
                else:
                    new_sequence += char
            sequence = new_sequence
        return sequence
    
    def _calculate_new_position(self) -> Tuple[int, int]:
        """Calculate new position based on current angle and step size"""
        angle_rad = math.radians(self.current_angle)
        new_x = self.current_pos[0] + self.step_size * math.cos(angle_rad)
        new_y = self.current_pos[1] + self.step_size * math.sin(angle_rad)
        return (round(new_x), round(new_y))
    
    def _interpret_sequence(self, sequence: str) -> Dict[Tuple[int, int], Room]:
        """Interpret L-System sequence to create rooms"""
        stack = []  # Stack for branching
        
        for char in sequence:
            if char == 'F':  # Move forward and create room
                new_pos = self._calculate_new_position()
                if new_pos not in self.rooms:
                    self.rooms[new_pos] = Room(new_pos[0], new_pos[1])
                    # Connect with previous room
                    if self.current_pos != new_pos:
                        self.rooms[self.current_pos].connections.append(new_pos)
                        self.rooms[new_pos].connections.append(self.current_pos)
                self.current_pos = new_pos
                
            elif char == '+':  # Turn right
                self.current_angle += self.angle
            elif char == '-':  # Turn left
                self.current_angle -= self.angle
            elif char == '[':  # Save current state
                stack.append((self.current_pos, self.current_angle))
            elif char == ']':  # Restore previous state
                self.current_pos, self.current_angle = stack.pop()
        
        return self.rooms
    
    def generate(self, iterations: int = 3) -> Dict[Tuple[int, int], Room]:
        """Generate dungeon layout using L-System"""
        self.rooms = {}
        self.current_pos = (0, 0)
        self.current_angle = 0
        
        # Create entrance room
        self.rooms[self.current_pos] = Room(0, 0, type="entrance")
        
        # Generate and interpret sequence
        sequence = self._apply_rules('S', iterations)
        rooms = self._interpret_sequence(sequence)
        
        # Set last generated room as exit
        last_pos = max(rooms.keys(), key=lambda x: x[0] + x[1])
        rooms[last_pos].type = "exit"
        
        # Add some treasure and monster rooms
        self._add_special_rooms()
        
        return self.rooms
    
    def _add_special_rooms(self):
        """Add treasure and monster rooms to the dungeon"""
        normal_rooms = [pos for pos, room in self.rooms.items() 
                       if room.type == "normal"]
        
        # Add treasure rooms (10% of normal rooms)
        treasure_count = max(1, len(normal_rooms) // 10)
        for pos in random.sample(normal_rooms, treasure_count):
            self.rooms[pos].type = "treasure"
            
        # Add monster rooms (20% of normal rooms)
        normal_rooms = [pos for pos, room in self.rooms.items() 
                       if room.type == "normal"]
        monster_count = max(1, len(normal_rooms) // 5)
        for pos in random.sample(normal_rooms, monster_count):
            self.rooms[pos].type = "monster"