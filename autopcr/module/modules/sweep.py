from abc import abstractmethod
from typing import List

from ...db.models import QuestDatum
from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...db.database import db
from ...model.enums import *
from ...model.custom import ItemType
from ...util.linq import flow

class explore_sweep(Module):
    @abstractmethod
    def remain_cnt(self, client: pcrclient) -> int: ...
    @abstractmethod
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int: ...
    @abstractmethod
    def not_max_stop(self): ...

    async def do_task(self, client: pcrclient):
        remain_cnt = self.remain_cnt(client)
        if remain_cnt:
            quest_id = self.get_max_quest(client, sweep_available = True)
            if not quest_id:
                raise SkipError("不存在可扫荡的探索")
            max_quest = self.get_max_quest(client)
            if self.not_max_stop() and max_quest != quest_id:
                raise AbortError(f"最高级探索{max_quest}未通关，不扫荡\n如欲扫荡已通关的，请关闭【非最高不扫荡】")
            name = db.get_quest_name(quest_id)
            await client.training_quest_skip(quest_id, remain_cnt)
            self._log(f"{name}扫荡{remain_cnt}次")
        else:
            raise SkipError("今日已扫荡")

@description('自动扫荡可扫荡的最高等级的EXP探索')
@name('EXP探索')
@booltype("exp_not_max_stop", "非最高不扫荡", True)
@default(True)
class explore_exp(explore_sweep):
    def remain_cnt(self, client: pcrclient) -> int: 
        return client.data.training_quest_max_count.exp_quest - client.data.training_quest_count.exp_quest
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int:
        return client.data.get_max_quest_exp(sweep_available)
    def not_max_stop(self): 
        return self.get_config("exp_not_max_stop")

@description('自动扫荡可扫荡的最高等级的Mana探索')
@name('Mana探索')
@booltype("mana_not_max_stop", "非最高不扫荡", True)
@default(True)
class explore_mana(explore_sweep):
    def remain_cnt(self, client: pcrclient) -> int: 
        return client.data.training_quest_max_count.gold_quest - client.data.training_quest_count.gold_quest
    def get_max_quest(self, client: pcrclient, sweep_available: bool = False) -> int:
        return client.data.get_max_quest_mana(sweep_available)
    def not_max_stop(self): 
        return self.get_config("mana_not_max_stop")

@singlechoice("underground_sweep", "扫荡策略", "总是扫荡", ["非庆典留一次数", "总是扫荡"])
@booltype("underground_not_max_stop", "非最高不扫荡", True)
@booltype("secret_dungeon_stop", "特别地下城期间不扫荡", True)
@description('会选择最高级地下城扫荡，非庆典留一次数指非mana庆典时会位于地下城内不扫荡，以期庆典当天能扫荡两次，获得更多的mana，但第一次时需手动打一关以完成每日任务')
@name('地下城扫荡')
@default(True)
class underground_skip(Module):
    async def do_task(self, client: pcrclient):
        infos = await client.get_dungeon_info()
        if not infos.dungeon_cleared_area_id_list:
            infos.dungeon_cleared_area_id_list = []
        not_max_stop = self.get_config("underground_not_max_stop")
        always_sweep = self.get_config("underground_sweep") == "总是扫荡"
        secret_dungeon_stop = self.get_config("secret_dungeon_stop")

        def dungeon_name(id: int):
            return db.dungeon_area[id].dungeon_name

        def get_cleared_max_dungeon_id():
            return max([0] + [id for id in infos.dungeon_cleared_area_id_list if db.is_dungeon_id(id)])

        def get_max_dungeon_id():
            return (flow(db.dungeon_area.values())
                    .select(lambda x: x.dungeon_area_id)
                    .max()
                   )

        async def do_enter(now_id = None):
            id = get_cleared_max_dungeon_id() if not now_id else now_id
            if id > 0:
                if not await client.is_deck_empty(ePartyType.DUNGEON):
                    await client.deck_update(ePartyType.DUNGEON, [0, 0, 0, 0, 0])
                await client.enter_dungeon(id)
                self._log(f"已进入【{dungeon_name(id)}】")
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        async def do_sweep(now_id = None):
            id = get_cleared_max_dungeon_id() if not now_id else now_id
            if id > 0:
                if id not in infos.dungeon_cleared_area_id_list:
                    raise AbortError(f"【{dungeon_name(id)}】未讨伐，无法扫荡")
                reward_list = await client.skip_dungeon(id)
                rewards = [reward for reward_item in reward_list.skip_result_list for reward in reward_item.reward_list 
                           if db.is_unit_memory((reward.type, reward.id)) 
                           or db.xinsui == (reward.type, reward.id)
                           or db.xingqiubei == (reward.type, reward.id)]
                result = await client.serialize_reward_summary(rewards)
                self._log(f"扫荡了【{dungeon_name(id)}】,获得了:\n{result}")
                return reward_list.rest_challenge_count[0].count
            else:
                raise AbortError("不存在已完成讨伐的地下城")

        double_mana = client.data.is_dungeon_mana_campaign()
        rest = infos.rest_challenge_count[0].count
        if infos.enter_area_id != 0:
            if db.is_secret_dungeon_id(infos.enter_area_id):
                raise SkipError("当前位于里地下城")

            self._log(f"当前位于【{dungeon_name(infos.enter_area_id)}】")
            if double_mana:
                self._log(f"今日地下城双倍mana")
                rest = await do_sweep(infos.enter_area_id)
            else:
                self._log(f"今日地下城非双倍mana")
                if rest:
                    self._log(f"还有{rest}次挑战次数，进行扫荡")
                    rest = await do_sweep(infos.enter_area_id)
                else:
                    if always_sweep:
                        rest = await do_sweep(infos.enter_area_id)

        if secret_dungeon_stop and db.is_secret_dungeon_time():
            raise SkipError("今日里地下城活动，不扫荡普通地下城")

        if rest:
            if not_max_stop and get_max_dungeon_id() != get_cleared_max_dungeon_id():
                raise AbortError(f"最高级地下城【{dungeon_name(get_max_dungeon_id())}】未通关，不扫荡\n如欲扫荡已通关的，请关闭【非最高不扫荡】")
            if double_mana or always_sweep:
                await do_sweep()
            else:
                await do_enter()
        else:
            raise SkipError("今日已扫荡地下城")

@booltype("secret_dungeon_retreat", "自动撤退", False)
@description('只进入特别地下城，以期扫荡前5层。需首通一次。自动撤退指首通后，当前位于特别地下城，且还有挑战次数，则会撤退后再次进入，以扫荡前5层，用于只打30层。')
@name('特别地下城扫荡')
@default(True)
class special_underground_skip(Module):
    async def do_task(self, client: pcrclient):
        if not db.is_secret_dungeon_time():
            raise SkipError("当前无特别地下城")

        infos = await client.get_dungeon_info()

        special_dungeon_area = db.get_open_secret_dungeon_area()
        _special_info = None
        secret_dungeon_retreat = self.get_config("secret_dungeon_retreat")
        async def special_dungeon_info(refresh: bool = False):
            nonlocal _special_info
            if refresh or not _special_info:
                _special_info = await client.get_special_dungeon_info(special_dungeon_area)
            return _special_info

        def dungeon_name(id: int):
            if id in db.dungeon_area:
                return db.dungeon_area[id].dungeon_name
            elif id in db.secret_dungeon_area:
                return db.secret_dungeon_area[id].dungeon_name
            else:
                return f"未知地下城{id}"

        async def do_retreat(id: int):
            await client.reset_special_dungeon(id)
            self._log(f"从【{dungeon_name(id)}】撤退")

        async def do_enter(id):
            if db.secret_dungeon_area[id].open_area_id not in infos.dungeon_cleared_area_id_list:
                raise AbortError(f"【{dungeon_name(id)}】未讨伐，无法进入特别地下城")

            await special_dungeon_info(refresh=True)
            if not await client.is_deck_empty(ePartyType.DUNGEON):
                await client.deck_update(ePartyType.DUNGEON, [0, 0, 0, 0, 0])

            req = await client.enter_special_dungeon(id)
            reward_list = req.skip_result_list if req.skip_result_list else []
            rewards = [reward for reward_item in reward_list for reward in reward_item.reward_list]
            result = await client.serialize_reward_summary(rewards)
            self._log(f"进入了【{dungeon_name(id)}】,获得了:\n{result}")

        rest = infos.rest_challenge_count[0].count

        if infos.enter_area_id != 0:
            if not db.is_secret_dungeon_id(infos.enter_area_id):
                raise AbortError("当前位于普通地下城，不支持扫荡")

            self._log(f"当前位于【{dungeon_name(infos.enter_area_id)}】")
            if rest:
                if secret_dungeon_retreat:
                    if (await special_dungeon_info()).clear_num == 0:
                        raise AbortError("特别地下城未通关，将不撤退")
                    await do_retreat(infos.enter_area_id)
                else:
                    raise AbortError("今天仍有挑战次数，但设置不撤退")

                        
        if rest:
            await do_enter(special_dungeon_area)

        if (await special_dungeon_info()).clear_num == 0:
            raise AbortError("特别地下城尚未首通，请记得通关")

        if not rest:
            raise SkipError("今日已扫荡特别地下城")


class investigate_sweep(Module):
    @abstractmethod
    def quest_data(self) -> List[QuestDatum]: ...
    @abstractmethod
    def campaign_times(self, client: pcrclient) -> int: ...
    @abstractmethod
    def required_count(self, client: pcrclient) -> int: ...
    @abstractmethod
    def stored_count(self, client: pcrclient) -> int: ...
    @abstractmethod
    def material_name(self) -> str: ...
    @abstractmethod
    def config_key(self, campaign_times: int) -> str: ...

    async def do_task(self, client: pcrclient):
        book_count = self.get_config(self.config_key(self.campaign_times(client)))
        if book_count <= 0:
            raise SkipError(f"{self.material_name()}扫荡本数为0")

        if self.stored_count(client) >= self.required_count(client):
            raise SkipError(f"{self.material_name()}需求已满足")

        quests = [quest for quest in self.quest_data() if client.data.is_quest_sweepable(quest.quest_id)]
        if not quests:
            raise SkipError(f"没有已通关的{self.material_name()}关卡")

        max_book_count = len(quests) * 4
        planned_count = min(book_count, max_book_count)
        if planned_count < book_count:
            self._log(f"当前只有{len(quests)}本已通关，扫荡本数由{book_count}调整为{planned_count}")

        target_count = {}
        rewards = []
        clear_count = 0
        no_stamina = False
        for index in range(planned_count):
            if self.stored_count(client) >= self.required_count(client):
                break

            quest = quests[index % len(quests)]
            daily_limit = max(1, quest.daily_limit)
            target_count[quest.quest_id] = target_count.get(quest.quest_id, 0) + daily_limit
            try:
                result, current_clear_count, no_stamina = await client.quest_skip_aware(
                    quest.quest_id,
                    target_count[quest.quest_id],
                    recover=True,
                    is_total=True,
                )
            except SkipError:
                continue

            rewards.extend(result)
            clear_count += current_clear_count
            if no_stamina:
                break

        if not clear_count:
            if no_stamina:
                raise SkipError(f"{self.material_name()}关卡体力不足")
            raise SkipError(f"没有可扫荡的{self.material_name()}关卡次数")

        msg = await client.serialize_reward_summary(rewards)
        self._log(f"按高到低扫荡{planned_count}本（含重置轮次），实际刷取{clear_count}次，获得了{msg}")


def _heart_book_candidates() -> List[int]:
    return list(range(len(db.heart_piece_quest) * 4 + 1))


def _star_cup_book_candidates() -> List[int]:
    return list(range(len(db.star_cup_quest) * 4 + 1))


@description('按心碎关卡从高到低扫荡。配置刷取关卡数，超过当前关卡数则从最高本重置刷下一轮，需求已满足时不刷。')
@name('心碎扫荡')
@conditional_not_execution('force_stop_heart_sweep', [], desc='不刷心碎庆典')
@inttype('xinsui_sweep_no_campaign_books', '无庆典刷前几本', 2, _heart_book_candidates)
@inttype('xinsui_sweep_2x_campaign_books', '2倍庆典刷前几本', 2, _heart_book_candidates)
@inttype('xinsui_sweep_3x_campaign_books', '3倍及以上庆典刷前几本', 2, _heart_book_candidates)
@default(True)
@tag_stamina_consume
class xinsui_sweep(investigate_sweep):
    def quest_data(self) -> List[QuestDatum]:
        return db.heart_piece_quest

    def campaign_times(self, client: pcrclient) -> int:
        return client.data.get_heart_piece_campaign_times()

    def required_count(self, client: pcrclient) -> int:
        return client.data.get_suixin_demand()[1]

    def stored_count(self, client: pcrclient) -> int:
        return client.data.get_inventory(db.xinsui) + client.data.get_inventory(db.heart) * 10

    def material_name(self) -> str:
        return '心碎'

    def config_key(self, campaign_times: int) -> str:
        if campaign_times <= 1:
            return 'xinsui_sweep_no_campaign_books'
        if campaign_times == 2:
            return 'xinsui_sweep_2x_campaign_books'
        return 'xinsui_sweep_3x_campaign_books'


@description('按星球杯关卡从高到低扫荡。配置值为关卡本数，超过当前本数后继续从最高本开始下一轮，最多支持3次重置。需求已满足时不刷。')
@name('星球杯扫荡')
@conditional_not_execution('force_stop_star_cup_sweep', [], desc='不刷星球杯庆典')
@inttype('starcup_sweep_no_campaign_books', '无庆典刷前几本', 0, _star_cup_book_candidates)
@inttype('starcup_sweep_2x_campaign_books', '2倍庆典刷前几本', 0, _star_cup_book_candidates)
@inttype('starcup_sweep_3x_campaign_books', '3倍及以上庆典刷前几本', 0, _star_cup_book_candidates)
@default(False)
@tag_stamina_consume
class starcup_sweep(investigate_sweep):
    def quest_data(self) -> List[QuestDatum]:
        return db.star_cup_quest

    def campaign_times(self, client: pcrclient) -> int:
        return client.data.get_star_cup_campaign_times()

    def required_count(self, client: pcrclient) -> int:
        return client.data.get_xingqiubei_demand()

    def stored_count(self, client: pcrclient) -> int:
        return client.data.get_inventory(db.xingqiubei)

    def material_name(self) -> str:
        return '星球杯'

    def config_key(self, campaign_times: int) -> str:
        if campaign_times <= 1:
            return 'starcup_sweep_no_campaign_books'
        if campaign_times == 2:
            return 'starcup_sweep_2x_campaign_books'
        return 'starcup_sweep_3x_campaign_books'
