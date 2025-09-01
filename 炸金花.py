import hashlib
import time
import random
from datetime import datetime

class OfflineGoldenFlower:
    def __init__(self):
        # 创建一副牌（52张，不包括大小王）
        self.suits = ['♠', '♥', '♣', '♦']  # 黑桃、红心、梅花、方块
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = []
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(f"{suit}{rank}")
        # 设置最大玩家数量（52张牌，每人3张，最多17人）
        self.max_players = 17
    
    def get_midnight_timestamp(self):
        """获取当天零点的时间戳"""
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day, 0, 0, 0)
        return int(midnight.timestamp())
    
    def generate_random_seed(self, round_number, player_random):
        """使用当天零点时间戳、局数和玩家随机数生成随机种子"""
        midnight_timestamp = self.get_midnight_timestamp()
        # 将时间戳、局数和玩家随机数首尾相连
        seed_value_str = str(midnight_timestamp) + str(round_number) + str(player_random)
        # 使用SHA-256哈希算法生成随机种子
        hash_object = hashlib.sha256(seed_value_str.encode())
        hex_dig = hash_object.hexdigest()
        # 将哈希值转换为整数
        return int(hex_dig, 16)
    
    def shuffle_deck(self, seed):
        """使用随机种子洗牌"""
        random.seed(seed)
        shuffled_deck = self.deck.copy()
        random.shuffle(shuffled_deck)
        return shuffled_deck
    
    def get_player_cards(self, shuffled_deck, player_num):
        """根据玩家编号获取对应的牌"""
        # 玩家编号从1开始，每个玩家3张牌
        start_index = (player_num - 1) * 3
        end_index = start_index + 3
        return shuffled_deck[start_index:end_index]
    
    def display_cards(self, cards):
        """显示牌面"""
        return ", ".join(cards)
    
    def play_round(self, player_num, player_random, round_number):
        """进行一局游戏"""
        # 生成随机种子并洗牌
        seed = self.generate_random_seed(round_number, player_random)
        shuffled_deck = self.shuffle_deck(seed)
        
        # 获取当前玩家的牌
        player_cards = self.get_player_cards(shuffled_deck, player_num)
        
        print(f"\n===== 第 {round_number} 局 =====")
        print(f"玩家 {player_num} 的牌：{self.display_cards(player_cards)}")
        print(f"随机种子：{seed}")
    
    def run(self):
        print("==================== 多人离线炸金花游戏 ====================")
        print("游戏规则：")
        print("1. 每位玩家选择自己的玩家编号（1、2、3...）")
        print(f"2. 最多支持 {self.max_players} 位玩家（每人3张牌，共52张牌）")
        print("3. 所有玩家输入相同的随机数（由玩家自行决定）")
        print("4. 每局开始前，所有玩家输入相同的局数")
        print("5. 系统会根据随机数，时间戳和局数生成随机牌，每位玩家获得3张不重复的牌")
        print("============================================================")
        
        # 获取玩家编号（只需一次）
        while True:
            try:
                player_num = int(input(f"请输入您的玩家编号（1-{self.max_players}）："))
                if player_num < 1:
                    print("玩家编号必须大于0！")
                    continue
                if player_num > self.max_players:
                    print(f"玩家编号不能超过{self.max_players}！（一副牌只有52张，每人3张，最多支持{self.max_players}位玩家）")
                    continue
                break
            except ValueError:
                print("请输入有效的数字！")
        
        # 获取随机数（只需一次）
        while True:
            try:
                player_random = input("请输入随机数（只需输入一次）：")
                if not player_random:
                    print("随机数不能为空！")
                    continue
                break
            except ValueError:
                print("请输入有效的随机数！")
        
        print(f"\n玩家编号：{player_num}")
        print(f"随机数：{player_random}")
        print("\n游戏开始！")
        
        # 游戏主循环
        while True:
            # 获取局数
            while True:
                try:
                    round_number = int(input("\n请输入局数："))
                    if round_number < 1:
                        print("游戏结束，谢谢参与！")
                        return
                    break
                except ValueError:
                    print("请输入有效的数字！")
            
            # 进行一局游戏
            self.play_round(player_num, player_random, round_number)

if __name__ == "__main__":
    game = OfflineGoldenFlower()
    game.run()
