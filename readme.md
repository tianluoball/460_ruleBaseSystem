# Procedural Dungeon Generator

A hybrid rule-based system that combines L-Systems and Grammar-based generation to create procedurally generated dungeons with coherent layouts and thematic descriptions.

## Features
- Procedural dungeon layout generation using L-Systems
- Theme-based room descriptions using grammar rules and random events
- Interactive web interface for visualization
- Connected narrative elements and progressive story development based on the distance from entrance

## Project Structure
```
project/
├── backend/
│   ├── src/
│   │   ├── dungeon_lsystem.py    # L-System for layout generation
│   │   ├── dungeon_grammar.py    # Grammar system for descriptions
│   │   └── dungeon_visualizer.py # SVG visualization
│   ├── api.py                    # FastAPI backend service
│   └── requirements.txt          # Python dependencies
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── DungeonGenerator.tsx # React component
    │   └── App.tsx
    └── package.json
```

## Installation

### Backend Setup
1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:
```bash
python api.py
```

### Frontend Setup
1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Usage
1. Open the web interface in your browser
2. Click the "Generate Dungeon" button to create a new dungeon
3. Click on rooms to view their descriptions
4. The legend shows different room types:
   - S (Green): Entrance
   - M (Purple): Monster Room
   - T (Yellow): Treasure Room
   - X (Red): Exit

## API Documentation
- GET `/api/generate-dungeon`: Generates a new dungeon
  - Returns: JSON containing SVG layout, room descriptions, theme, and story elements

## Dependencies
### Backend
- FastAPI
- svgwrite
- uvicorn

### Frontend
- React
- TypeScript
- Vite

## Live Demo
The project is deployed at: https://tianluoball.github.io/460_ruleBaseSystem/

## License
MIT License