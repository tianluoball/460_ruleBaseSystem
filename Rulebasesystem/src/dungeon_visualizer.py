import svgwrite
from typing import Dict, Tuple, Union
from .dungeon_lsystem import Room

class DungeonVisualizer:
    def __init__(self, cell_size: int = 50):
        self.cell_size = cell_size
        self.colors = {
            'entrance': '#4CAF50',  # Green
            'exit': '#F44336',      # Red
            'normal': '#9E9E9E',    # Grey
            'treasure': '#FFD700',   # Gold
            'monster': '#7B1FA2'     # Purple
        }
        self.connection_color = '#616161'
        
    def _normalize_coordinates(self, rooms: Dict[Tuple[int, int], Room]) -> Tuple[Dict[Tuple[int, int], Room], int, int]:
        """Normalize room coordinates to start from (0,0)"""
        if not rooms:
            return rooms, 0, 0
            
        min_x = min(x for x, _ in rooms.keys())
        min_y = min(y for _, y in rooms.keys())
        
        normalized_rooms = {}
        for (x, y), room in rooms.items():
            new_x, new_y = x - min_x, y - min_y
            new_room = Room(new_x, new_y, room.type)
            new_room.connections = [(cx - min_x, cy - min_y) for cx, cy in room.connections]
            normalized_rooms[(new_x, new_y)] = new_room
            
        max_x = max(x for x, _ in normalized_rooms.keys())
        max_y = max(y for _, y in normalized_rooms.keys())
        
        return normalized_rooms, max_x + 1, max_y + 1

    def create_svg(self, rooms: Dict[Tuple[int, int], Room], filename: str = None, 
                  return_string: bool = False, return_normalized: bool = False) -> Union[str, Tuple[str, Dict]]:
        """Create SVG visualization of the dungeon"""
        # Normalize coordinates
        normalized_rooms, width, height = self._normalize_coordinates(rooms)
        
        # Calculate SVG dimensions
        svg_width = (width + 1) * self.cell_size
        svg_height = (height + 1) * self.cell_size
        
        # Create SVG document
        dwg = svgwrite.Drawing(filename=filename if filename else 'dummy.svg',
                             size=(svg_width, svg_height))
        
        # Add background
        dwg.add(dwg.rect(insert=(0, 0), size=(svg_width, svg_height), fill='#424242'))
        
        # Draw connections first
        for (x, y), room in normalized_rooms.items():
            start_x = (x + 0.5) * self.cell_size
            start_y = (y + 0.5) * self.cell_size
            
            for conn_x, conn_y in room.connections:
                if (conn_x, conn_y) > (x, y):  # Only draw each connection once
                    end_x = (conn_x + 0.5) * self.cell_size
                    end_y = (conn_y + 0.5) * self.cell_size
                    dwg.add(dwg.line(
                        start=(start_x, start_y),
                        end=(end_x, end_y),
                        stroke=self.connection_color,
                        stroke_width=3
                    ))
        
        # Draw rooms
        for (x, y), room in normalized_rooms.items():
            center_x = (x + 0.5) * self.cell_size
            center_y = (y + 0.5) * self.cell_size
            
            # Room circle
            circle = dwg.circle(
                center=(center_x, center_y),
                r=self.cell_size // 3,
                fill=self.colors[room.type],
                stroke='white',
                stroke_width=2
            )
            dwg.add(circle)
            
            # Room type label
            if room.type != 'normal':
                text = dwg.text(
                    room.type[0].upper(),
                    insert=(center_x, center_y),
                    font_size=self.cell_size // 4,
                    font_family='Arial',
                    fill='white',
                    text_anchor='middle',
                    dominant_baseline='middle'
                )
                dwg.add(text)
        
        if return_normalized:
            return dwg.tostring(), normalized_rooms
        elif return_string:
            return dwg.tostring()
        elif filename:
            dwg.save()
            return ""