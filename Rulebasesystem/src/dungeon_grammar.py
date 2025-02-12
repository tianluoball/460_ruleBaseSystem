import random
from typing import Dict, List, Tuple, Optional
from enum import Enum

class DungeonTheme(Enum):
    ANCIENT_TEMPLE = "Ancient Temple"
    ABANDONED_MINE = "Abandoned Mine"
    CURSED_CRYPT = "Cursed Crypt"
    DRAGON_LAIR = "Dragon's Lair"

class DungeonGrammar:
    def __init__(self):
        self.current_theme = random.choice(list(DungeonTheme))
        
        # Story tracking
        self.story_state = {
            'main_treasure': random.choice(['the Sacred Chalice', 'the Eternal Flame', 'the Crystal of Power']),
            'main_villain': None,
            'discovered_clues': [],
            'treasure_count': 0,
            'last_monster': None,
            'quest_progress': 0,
            'revealed_rooms': set()  # Track which rooms have been explored
        }
        
        # Theme-specific content
        self.themes = {
            DungeonTheme.ANCIENT_TEMPLE: {
                'description': [
                    "An ancient temple dedicated to forgotten gods, its halls still resonating with mystical energy.",
                    "A sacred sanctuary lost to time, where divine artifacts remain under eternal guard.",
                    "Once a place of worship, now a labyrinth of holy chambers and divine trials."
                ],
                'atmosphere': ["sacred", "mysterious", "divine"],
                'objects': ["altars", "statues", "holy relics"],
                'enemies': ["stone guardians", "corrupted priests", "temple sentinels"]
            },
            DungeonTheme.ABANDONED_MINE: {
                'description': [
                    "A forsaken mine where precious gems once lured countless fortune seekers.",
                    "Deep mine shafts that hide both valuable minerals and untold dangers.",
                    "An extensive network of tunnels, abandoned after mysterious incidents."
                ],
                'atmosphere': ["dark", "damp", "claustrophobic"],
                'objects': ["mine carts", "pickaxes", "gem veins"],
                'enemies': ["cave spiders", "hostile automatons", "mutated miners"]
            },
            DungeonTheme.CURSED_CRYPT: {
                'description': [
                    "An ancient burial ground where restless spirits roam the halls.",
                    "A maze of tombs and sarcophagi, each hiding centuries of dark secrets.",
                    "The final resting place of powerful sorcerers, their magic still lingers."
                ],
                'atmosphere': ["eerie", "haunted", "foreboding"],
                'objects': ["sarcophagi", "urns", "burial treasures"],
                'enemies': ["wraiths", "skeletal warriors", "cursed guardians"]
            },
            DungeonTheme.DRAGON_LAIR: {
                'description': [
                    "A vast cavern system where an ancient dragon has made its home.",
                    "Scorched halls filled with treasures from countless realms.",
                    "A legendary dragon's domain, where few adventurers dare to tread."
                ],
                'atmosphere': ["scorched", "grand", "dangerous"],
                'objects': ["treasure hoards", "dragon eggs", "melted weapons"],
                'enemies': ["young dragons", "drake handlers", "fire elementals"]
            }
        }

        # Room type descriptions
        self.rules = {
            'entrance': {
                'description': [
                    "A grand archway marks the entrance, ancient runes pulsing with faint light.",
                    "A heavy stone door stands before you, its surface carved with intricate symbols.",
                    "A mysterious portal serves as the gateway, its edges shimmer with magical energy."
                ],
                'details': [
                    "Warning glyphs flicker on the surrounding walls.",
                    "The remnants of previous expeditions litter the ground.",
                    "A mystical barrier ripples as you pass through."
                ]
            },
            'normal': {
                'description': [
                    "A spacious chamber with weathered stone walls.",
                    "A modest room with architectural elements typical of its era.",
                    "An unremarkable passage intersection that has stood the test of time."
                ],
                'details': [
                    "The echo of water droplets fills the silence.",
                    "Layers of ancient dust cover the floor.",
                    "Broken pieces of pottery suggest former habitation."
                ]
            },
            'monster': {
                'description': [
                    "A chamber emanating an aura of danger.",
                    "A room marked by signs of fierce combat.",
                    "A lair showing clear signs of creature habitation."
                ],
                'monster_type': {
                    DungeonTheme.ANCIENT_TEMPLE: ["a stone guardian", "a corrupted priest", "a temple sentinel"],
                    DungeonTheme.ABANDONED_MINE: ["a cave spider", "a malfunctioning golem", "a mutated miner"],
                    DungeonTheme.CURSED_CRYPT: ["a vengeful wraith", "a skeletal warrior", "a cursed guardian"],
                    DungeonTheme.DRAGON_LAIR: ["a young drake", "a fire elemental", "a dragon's servant"]
                },
                'details': [
                    "The air is thick with the scent of danger.",
                    "Fresh claw marks score the walls.",
                    "Eerie sounds echo from the shadows."
                ]
            },
            'treasure': {
                'description': [
                    "An opulent chamber clearly designed to house valuables.",
                    "A secure vault sealed by ancient magic.",
                    "A hidden treasury untouched for centuries."
                ],
                'treasure_type': {
                    DungeonTheme.ANCIENT_TEMPLE: ["a sacred artifact", "a blessed chalice", "a divine relic"],
                    DungeonTheme.ABANDONED_MINE: ["a perfect gemstone", "a chest of precious ores", "ancient mining tools"],
                    DungeonTheme.CURSED_CRYPT: ["a cursed amulet", "an ancient sarcophagus", "forbidden scrolls"],
                    DungeonTheme.DRAGON_LAIR: ["a dragon's hoard", "enchanted weaponry", "royal treasures"]
                },
                'details': [
                    "Golden particles float in the air.",
                    "Precious gems reflect your torch light.",
                    "The floor is inlaid with valuable materials."
                ]
            },
            'exit': {
                'description': [
                    "A pathway leading back to the surface.",
                    "A magical portal offering escape.",
                    "An ancient mechanism revealing the way out."
                ],
                'details': [
                    "Fresh air streams in from above.",
                    "Ancient runes of protection guard the exit.",
                    "A shaft of natural light pierces the darkness."
                ]
            }
        }

    def get_connected_rooms_info(self, pos: Tuple[int, int], rooms: Dict) -> List[str]:
        """Get information about connected rooms"""
        connected_info = []
        x, y = pos
        
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            check_pos = (x + dx, y + dy)
            if check_pos in rooms and check_pos not in self.story_state['revealed_rooms']:
                room = rooms[check_pos]
                if room.type == 'monster':
                    connected_info.append("Menacing sounds echo from nearby")
                elif room.type == 'treasure':
                    connected_info.append("A faint golden glow seeps through one of the exits")
                elif room.type == 'exit':
                    connected_info.append("A fresh breeze flows from one direction")
        
        return connected_info

    def update_story_progress(self, room_type: str, pos: Tuple[int, int]) -> str:
        """Update story progress based on room discovery"""
        self.story_state['revealed_rooms'].add(pos)
        
        if room_type == 'monster':
            if not self.story_state['main_villain']:
                self.story_state['main_villain'] = random.choice(
                    self.rules['monster_type'][self.current_theme]
                )
                return f"Legends speak of {self.story_state['main_villain']} guarding {self.story_state['main_treasure']}"
        
        elif room_type == 'treasure':
            self.story_state['treasure_count'] += 1
            if self.story_state['treasure_count'] == 1:
                clue = f"Ancient writings mention {self.story_state['main_treasure']} hidden in these depths"
                self.story_state['discovered_clues'].append(clue)
                return clue
        
        return ""

    def generate_dungeon_overview(self) -> str:
        """Generate an overview description of the dungeon"""
        theme_data = self.themes[self.current_theme]
        overview = f"""
Welcome to the {self.current_theme.value}!

{random.choice(theme_data['description'])}

The atmosphere here is {random.choice(theme_data['atmosphere'])}, with {random.choice(theme_data['objects'])} scattered throughout.
Be wary of {random.choice(theme_data['enemies'])} that lurk in the shadows.

Legend speaks of {self.story_state['main_treasure']} hidden within these halls...

(Click on individual rooms to explore their details)
"""
        return overview

    def generate_description_by_distance(self, distance: int) -> str:
        """Generate description based on distance from entrance"""
        if distance < 3:
            return "The torches here are fresh, indicating frequent visits"
        elif distance < 5:
            return "Cobwebs grow thicker in these less-traveled halls"
        else:
            return "The ancient air here suggests this area hasn't been visited in ages"

    def generate_event(self) -> str:
        """Generate a random event description"""
        events = {
            'trap': {
                'trigger': "You step on a loose tile",
                'consequence': ["arrows shoot from the walls", "the floor suddenly gives way", "poisonous gas begins to spread"],
                'solution': ["you quickly jump back", "block it with your shield", "find the mechanism to disable it"]
            },
            'discovery': {
                'trigger': "You find the remains of a previous explorer",
                'items': ["a weathered journal", "a mysterious map", "a rusted key"],
                'clue': f"Their notes mention {self.story_state['main_treasure']}"
            }
        }
        
        event_type = random.choice(list(events.keys()))
        event = events[event_type]
        
        if event_type == 'trap':
            return f"CAUTION: {event['trigger']} and {random.choice(event['consequence'])}, but {random.choice(event['solution'])}."
        else:
            return f"DISCOVERY: {event['trigger']} holding {random.choice(event['items'])}. {event['clue']}."

    def generate_room_description(self, room_type: str, pos: Tuple[int, int], entrance_pos: Tuple[int, int], rooms: Dict) -> str:
        """Generate description for a specific room, considering theme and context"""
        if room_type not in self.rules:
            return "A plain chamber."
            
        # Calculate distance from entrance
        distance = abs(pos[0] - entrance_pos[0]) + abs(pos[1] - entrance_pos[1])
        distance_desc = self.generate_description_by_distance(distance)
        
        # Generate base description
        room_rules = self.rules[room_type]
        description = random.choice(room_rules['description'])
        details = random.choice(room_rules['details'])
        
        # Add theme-specific content for special rooms
        if room_type == 'monster':
            monster = random.choice(room_rules['monster_type'][self.current_theme])
            full_desc = f"{description} {distance_desc}. {details} {monster} lurks within."
        elif room_type == 'treasure':
            treasure = random.choice(room_rules['treasure_type'][self.current_theme])
            full_desc = f"{description} {distance_desc}. {details} In the center, {treasure} draws your attention."
        else:
            full_desc = f"{description} {distance_desc}. {details}"
        
        # Add connected rooms info
        connected_info = self.get_connected_rooms_info(pos, rooms)
        if connected_info:
            full_desc += f" {random.choice(connected_info)}."
        
        # Add story progress
        story_update = self.update_story_progress(room_type, pos)
        if story_update:
            full_desc += f" {story_update}."
        
        # Add random event with 30% chance
        if random.random() < 0.3:
            full_desc += " " + self.generate_event()
            
        return full_desc

    def generate_dungeon_descriptions(self, rooms: Dict) -> Dict[tuple, str]:
        """Generate descriptions for all rooms in the dungeon"""
        entrance_pos = next((pos for pos, room in rooms.items() if room.type == 'entrance'), (0, 0))
        descriptions = {}
        for pos, room in rooms.items():
            descriptions[pos] = self.generate_room_description(room.type, pos, entrance_pos, rooms)
        return descriptions