from __future__ import annotations

from typing import Any, Iterable


JJC_TALENT_SKILL_LEVELS = {slot: 1000 for slot in range(1, 6)}
JJC_TALENT_SKILL_NODE_LEVELS = {638: 5}
JJC_MASTER_SKILL_NODE_LEVELS = {99: 1}
JJC_ROLE_MASTERY = {
    **{
        group * 100 + slot: (4, 4)
        for group in range(101, 109)
        for slot in range(1, 5)
    },
    10504: (5, 2),
    99999: (4, 4),
}


def progression_kwargs() -> dict[str, Any]:
    return {
        "talent_skill_levels": dict(JJC_TALENT_SKILL_LEVELS),
        "talent_skill_node_levels": dict(JJC_TALENT_SKILL_NODE_LEVELS),
        "master_skill_node_levels": dict(JJC_MASTER_SKILL_NODE_LEVELS),
        "role_mastery": dict(JJC_ROLE_MASTERY),
        "talent_full_info": False,
    }


def _unit_payload(unit_id: int) -> dict[str, Any]:
    return {
        "enemyid": 0,
        "unitId": int(unit_id),
        "level": 1,
        "rarity": 1,
        "love": 0,
        "rank": 1,
        "equipLevel": [-1, -1, -1, -1, -1, -1],
        "skillLevel": [1, 1, 1, 1],
        "playLoveDic": {},
        "uniqueEqLv": 0,
        "uniqueEq2Lv": -1,
        "exEquip": [0, 0, 0],
        "exEquipLevel": [0, 0, 0],
        "exEquipSubs": {},
        "PrefabId": 0,
        "love2": 0,
    }


def build_battle_request(
    player_ids: Iterable[int],
    enemy_ids: Iterable[int],
    repeat_count: int,
) -> dict[str, Any]:
    if repeat_count <= 0:
        raise ValueError("repeat_count must be positive")
    role_mastery = {
        mastery_id: {"Item1": levels[0], "Item2": levels[1]}
        for mastery_id, levels in JJC_ROLE_MASTERY.items()
    }
    return {
        "CalcStats": 0,
        "PlayerList": [_unit_payload(value) for value in player_ids],
        "EnemyList": [_unit_payload(value) for value in enemy_ids],
        "GuildEnemyList": [],
        "UBExecTimeList": [],
        "SemanUBExecTimeList": [],
        "Settings": {
            "DataName": "默认世界线",
            "UseFixedRandomSeed": False,
            "RandomSeed": 666,
            "ForceNoCritical_player": False,
            "ForceNoCritical_enemy": False,
            "ForceIgnoreDodge_player": False,
            "ForceIgnoreDodge_enemy": False,
            "ForceCritical_player": False,
            "randomSpecialDatas": [],
        },
        "TalentSkillLevels": dict(JJC_TALENT_SKILL_LEVELS),
        "TalentSkillNodeLevels": dict(JJC_TALENT_SKILL_NODE_LEVELS),
        "MasterSkillNodeLevels": dict(JJC_MASTER_SKILL_NODE_LEVELS),
        "RoleMastery": role_mastery,
        "LabyrinthEnhancedNodeIds": [],
        "LabyrinthRelicIds": [],
        "LabyrinthAlphaRupee": 0,
        "BattleTime": 90,
        "TalentFullInfo": False,
        "IsTalentQuest": False,
        "ToMaxUnitAttr": True,
        "IsAutoMode": True,
        "IsSetMode": False,
        "IsSemanMode": False,
        "IsGuildBattle": False,
        "IsSkipping": True,
        "TimeLineData": None,
        "WaveGroupId": 0,
        "SetToggles": [False, False, False, False, False],
        "NeedOnceResult": False,
        "RepeatCount": int(repeat_count),
    }
