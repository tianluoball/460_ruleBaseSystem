import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
from src.dungeon_lsystem import DungeonLSystem
from src.dungeon_visualizer import DungeonVisualizer
from src.dungeon_grammar import DungeonGrammar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/generate-dungeon")
async def generate_dungeon():
    try:
        # initial grammar
        grammar = DungeonGrammar()
        
        # generate maps using Lsystem
        generator = DungeonLSystem()
        dungeon = generator.generate(iterations=3)
        
        # retrive overview description
        overview = grammar.generate_dungeon_overview()
        
        # get image and normalize location
        visualizer = DungeonVisualizer(cell_size=50)
        svg_content, normalized_rooms = visualizer.create_svg(dungeon, return_string=True, return_normalized=True)
        
        # get normalized location
        entrance_pos = next((pos for pos, room in normalized_rooms.items() if room.type == 'entrance'), (0, 0))
        
        # description attached on normalized location
        descriptions = {
            f"{pos[0]},{pos[1]}": grammar.generate_room_description(
                room.type, 
                pos, 
                entrance_pos,
                normalized_rooms
            )
            for pos, room in normalized_rooms.items()
        }
        
        # return all
        return JSONResponse(content={
            "svg": svg_content,
            "overview": overview,
            "descriptions": descriptions,
            "theme": grammar.current_theme.value,
            "mainTreasure": grammar.story_state['main_treasure']
        })
        
    except Exception as e:
        print("Error generating dungeon:", str(e))
        print("Traceback:", traceback.format_exc())
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")