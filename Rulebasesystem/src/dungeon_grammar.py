import random
from typing import Dict, List

class DungeonGrammar:
    def __init__(self):
        self.rules = {
            'entrance': {
                'description': [
                    "一个古老的石门入口，上面刻着神秘的符文。",
                    "一扇厚重的铁门，门边的火把闪烁着微弱的光芒。",
                    "一个布满藤蔓的拱形门廊，通向地下深处。"
                ],
                'details': [
                    "门边的墙上刻着警告的文字。",
                    "地面上散落着先前探险者留下的足迹。",
                    "潮湿的空气中弥漫着神秘的气息。"
                ]
            },
            'normal': {
                'description': [
                    "一个空旷的石室，墙壁上爬满了苔藓。",
                    "一个方形的房间，角落里堆积着碎石。",
                    "一处看似平常的通道交叉点。"
                ],
                'details': [
                    "房间里回荡着水滴的声音。",
                    "地上铺着厚厚的灰尘。",
                    "墙上的火把插座已经生锈。"
                ]
            },
            'monster': {
                'description': [
                    "一个充满危险气息的洞穴。",
                    "一个布满骨头碎片的黑暗房间。",
                    "一处明显是某种生物巢穴的区域。"
                ],
                'monster_type': [
                    "一群饥饿的地精",
                    "一只嗜血的食尸鬼",
                    "一个愤怒的石魔像"
                ],
                'details': [
                    "腐烂的气味弥漫在空气中。",
                    "地面上有可疑的爪痕。",
                    "黑暗中闪烁着危险的红色眼睛。"
                ]
            },
            'treasure': {
                'description': [
                    "一个装饰华丽的宝库。",
                    "一处被魔法封印的密室。",
                    "一个布满金币的藏宝室。"
                ],
                'treasure_type': [
                    "一个镶嵌宝石的古老宝箱",
                    "一堆闪闪发光的金币",
                    "一件神秘的魔法物品"
                ],
                'details': [
                    "空气中闪烁着金色的微粒。",
                    "墙上的宝石反射着微弱的光芒。",
                    "地面上铺着精美的马赛克。"
                ]
            },
            'exit': {
                'description': [
                    "一个通向地面的楼梯。",
                    "一道被魔法封印的出口。",
                    "一个古老的传送门。"
                ],
                'details': [
                    "新鲜的空气从这里飘来。",
                    "出口处刻着古老的祝福语。",
                    "一道光束从上方照射下来。"
                ]
            }
        }
    
    def generate_room_description(self, room_type: str) -> str:
        """生成特定类型房间的描述"""
        if room_type not in self.rules:
            return "一个普通的房间。"
            
        room_rules = self.rules[room_type]
        description = random.choice(room_rules['description'])
        details = random.choice(room_rules['details'])
        
        # 为特殊房间添加额外描述
        if room_type == 'monster':
            monster = random.choice(room_rules['monster_type'])
            return f"{description} {details} {monster}正在这里徘徊。"
        elif room_type == 'treasure':
            treasure = random.choice(room_rules['treasure_type'])
            return f"{description} {details} 在房间中央，{treasure}吸引着你的注意。"
        else:
            return f"{description} {details}"
            
    def generate_dungeon_descriptions(self, rooms: Dict) -> Dict[tuple, str]:
        """为整个地下城的所有房间生成描述"""
        descriptions = {}
        for pos, room in rooms.items():
            descriptions[pos] = self.generate_room_description(room.type)
        return descriptions