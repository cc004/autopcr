import sqlite3

class RecordDAO:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_training_quest_mana(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, start_time FROM training_quest_data WHERE area_id=21001",
            ).fetchall()
        return r

    def get_training_quest_exp(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, start_time FROM training_quest_data WHERE area_id=21002",
            ).fetchall()
        return r

    def get_clan_battle_period(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT clan_battle_id, start_time, end_time FROM clan_battle_period",
            ).fetchall()
        return r

    def get_chara_fortune_schedule(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT fortune_id, start_time, end_time FROM chara_fortune_schedule",
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

    def get_tower_area_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT max_floor_num, cloister_quest_id FROM tower_area_data",
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

    def get_unit_memory(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, unit_material_id FROM unit_rarity WHERE unit_id < 190000 GROUP BY unit_material_id"
            ).fetchall()
        return r

    def get_unlock_rarity_six(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, material_id FROM unlock_rarity_6 WHERE slot_id=1",
            ).fetchall()
        return r

    def get_memory_quest_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, reward_image_1 FROM quest_data WHERE quest_id>=12000000 and quest_id<13000000",
            ).fetchall()
            # shiori wait for stamina half and odd up
            # r += conn.execute(
            #     f"SELECT quest_id, drop_reward_id FROM shiori_quest WHERE drop_reward_id != 0",
            # ).fetchall()
        return r

    def get_six_area_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, reward_image_1 FROM quest_data WHERE quest_id>=13000000 and quest_id<14000000",
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

    def get_campaign_gacha(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT campaign_id, start_time, end_time FROM campaign_freegacha",
            ).fetchall()
        return r

    def get_campaign_gacha_info(self, campaign_id: int):
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

    def get_quest_name(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, quest_name FROM quest_data",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, quest_name FROM hatsune_quest",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, quest_name FROM shiori_quest",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, quest_name FROM training_quest_data",
            ).fetchall()
        return r
    
    def get_hatsune_item(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT event_id, boss_ticket_id, gacha_ticket_id FROM hatsune_item",
            ).fetchall()
        return r

    def get_quest_to_event(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT quest_id, event_id FROM hatsune_quest",
            ).fetchall()
            r += conn.execute(
                f"SELECT quest_id, event_id FROM shiori_quest",
            ).fetchall()
        return r

    def get_unit_rarity_consume(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, rarity, unit_material_id, consume_num FROM unit_rarity",
            ).fetchall()
            r += conn.execute(
                f"SELECT unit_id, 6, material_id, material_count FROM unlock_rarity_6 WHERE material_id!=25001",
            ).fetchall()
            r += conn.execute(
                f"SELECT unit_id, 6, material_id, SUM(material_count) FROM unlock_rarity_6 WHERE material_id=25001 GROUP BY unit_id",
            ).fetchall()
        return r

    def get_unit_unique_equip_id(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, equip_id FROM unit_unique_equip",
            ).fetchall()
        return r

    def get_unique_equip_consume(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT equip_id, 0, reward_type_1, item_id_1, consume_num_1, reward_type_2, item_id_2, consume_num_2 FROM unique_equipment_craft",
            ).fetchall()
            r += conn.execute(
                f"SELECT equip_id, 0, reward_type_2, item_id_2, consume_num_2 FROM unique_equipment_craft",
            ).fetchall()
            r += conn.execute(
                f"SELECT equip_id, unique_equip_rank, reward_type_1, item_id_1, consume_num_1, reward_type_2, item_id_2, consume_num_2 FROM unique_equipment_rankup",
            ).fetchall()
            r += conn.execute(
                f"SELECT equip_id, unique_equip_rank, reward_type_2, item_id_2, consume_num_2 FROM unique_equipment_rankup",
            ).fetchall()
        return r

    def get_campaign_schedule(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT id, campaign_category, value, start_time, end_time FROM campaign_schedule",
            ).fetchall()
        return r

    def get_hatsune_schedule(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT event_id, start_time, end_time FROM hatsune_schedule",
            ).fetchall()
        return r

    def get_unit_promotion(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT unit_id, promotion_level, equip_slot_1, equip_slot_2, equip_slot_3, equip_slot_4, equip_slot_5, equip_slot_6 FROM unit_promotion",
            ).fetchall()
        return r

    def get_equipment_craft(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT * FROM equipment_craft",
            ).fetchall()
        return r

    def get_unique_equipment_enhance_data(self):
        with self.connect() as conn:
            r = conn.execute(
                f"SELECT rank, enhance_level FROM unique_equipment_enhance_data",
            ).fetchall()
        return r
