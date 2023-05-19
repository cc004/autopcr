import sqlite3

class RecordDAO:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_clan_battle_period(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT clan_battle_id, start_time, end_time FROM clan_battle_period",
            ).fetchall()
        return r

    def get_main_story_detail(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT story_id, pre_story_id, unlock_quest_id, title FROM story_detail WHERE story_id >= 2000000 AND story_id < 3000000",
            ).fetchall()
        return r

    def get_tower_story_detail(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT story_id, pre_story_id, unlock_quest_id, title, start_time FROM tower_story_detail",
            ).fetchall()
        return r

    def get_team_max_stamina(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT team_level, max_stamina FROM experience_team",
            ).fetchall()
        return r

    def get_tower_quest_detail(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT tower_quest_id, floor_num FROM tower_quest_data",
            ).fetchall()
        return r

    def get_event_story_detail(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT story_id, pre_story_id, title FROM event_story_detail WHERE visible_type = 0",
            ).fetchall()
        return r

    def get_unit_story_detail(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT story_id, pre_story_id, story_group_id, love_level, title FROM story_detail WHERE story_id >= 1000000 AND story_id < 2000000",
            ).fetchall()
        return r

    def get_equitement_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT equipment_id, equipment_name FROM equipment_data",
            ).fetchall()
        return r

    def get_item_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT item_id, item_name FROM item_data",
            ).fetchall()
        return r

    def get_unit_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, unit_name FROM unit_data",
            ).fetchall()
        return r

    def get_room_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT id, name, max_level FROM room_item",
            ).fetchall()
        return r

    def get_unlock_rarity_six(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, material_id FROM unlock_rarity_6 WHERE slot_id=1",
            ).fetchall()
        return r

    def get_six_area_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, reward_image_1 FROM quest_data WHERE quest_id>13018000 and quest_id<13999999",
            ).fetchall()
        return r

    def get_daily_mission(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT daily_mission_id FROM daily_mission_data",
            ).fetchall()
        return r

    def get_tower_schedule(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT tower_schedule_id, start_time, end_time FROM tower_schedule",
            ).fetchall()
        return r

    def get_dungeon_name(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT dungeon_area_id, dungeon_name FROM dungeon_area",
            ).fetchall()
        return r

    def get_campaign(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT campaign_id, start_time, end_time FROM campaign_freegacha",
            ).fetchall()
        return r

    def get_campaign_gacha(self, campaign_id: int):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT gacha_id FROM campaign_freegacha_data WHERE campaign_id={campaign_id}",
            ).fetchall()
        return r

    def get_love_chara(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT love_level, total_love, rarity FROM love_chara",
            ).fetchall()
        return r

    def get_love_cake(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT item_id, value FROM item_data WHERE item_id >= 50000 AND item_id < 51000",
            ).fetchall()
        return r

    def get_quest_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, stamina, daily_limit FROM quest_data",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, stamina, daily_limit FROM hatsune_quest",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, stamina, daily_limit FROM shiori_quest",
            ).fetchall()
        return r
