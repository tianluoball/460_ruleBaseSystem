import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
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
        # 生成地下城
        generator = DungeonLSystem()
        dungeon = generator.generate(iterations=3)
        
        # 生成描述
        grammar = DungeonGrammar()
        
        # 创建可视化并获取规范化的房间坐标
        visualizer = DungeonVisualizer(cell_size=50)
        svg_content, normalized_rooms = visualizer.create_svg(dungeon, return_string=True, return_normalized=True)
        
        # 为规范化后的坐标生成描述
        descriptions_dict = {}
        for (x, y), room in normalized_rooms.items():
            descriptions_dict[f"{x},{y}"] = grammar.generate_room_description(room.type)
        
        print("Generated coordinates:", list(descriptions_dict.keys()))  # 调试用
        
        # 返回JSON响应
        return JSONResponse(content={
            "svg": svg_content,
            "descriptions": descriptions_dict
        })
        
    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")