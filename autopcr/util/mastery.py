from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from ..db.models import (
    UnitRoleMasteryId,
    UnitRoleMasteryItemDatum,
    UnitRoleMasteryLevel,
    UnitRoleMasterySlotDatum,
    UnitRoleType,
)
from ..model.enums import eInventoryType


UNIVERSAL_MASTERY_ITEMS = {level: 80000 + level for level in range(1, 6)}
DEFAULT_MASTERY_COSTS = [20, 40, 50, 60, 70, 90]


def _mastery_metadata() -> Dict[str, Any]:
    """Build calculator metadata from the currently loaded master database."""
    from ..db.database import db

    if db.dbmgr is None:
        raise ValueError("数据库未初始化完成，请先刷新账号数据")

    with db.dbmgr.session() as session:
        role_types = session.query(UnitRoleType).all()
        mastery_ids = session.query(UnitRoleMasteryId).all()
        slots = session.query(UnitRoleMasterySlotDatum).all()
        items = session.query(UnitRoleMasteryItemDatum).all()
        levels = session.query(UnitRoleMasteryLevel).all()

    slot_by_key = {(row.mastery_id, row.slot_level): row for row in slots}
    items_by_key = {(row.mastery_id, row.slot_level): row.item_id_1 for row in items}
    levels_by_key = defaultdict(dict)
    for row in levels:
        levels_by_key[(row.mastery_id, row.slot_level)][row.enhance_level] = row.num

    mastery: Dict[str, Dict[str, Any]] = defaultdict(dict)
    cost_candidates: List[List[int]] = []
    for row in mastery_ids:
        slot_rows = [slot_by_key.get((row.mastery_id, level)) for level in range(1, 6)]
        first_slot = next((slot for slot in slot_rows if slot is not None), None)
        costs = levels_by_key.get((row.mastery_id, 1), {})
        if costs:
            cost_candidates.append([costs.get(level, 0) for level in range(6)])
        mastery[str(row.unit_role_id)][str(row.slot_id)] = {
            "name": first_slot.name if first_slot else f"槽位{row.slot_id}",
            "items": {
                str(level): items_by_key[(row.mastery_id, level)]
                for level in range(1, 6)
                if (row.mastery_id, level) in items_by_key
            },
        }

    costs = next((candidate for candidate in cost_candidates if all(candidate)), None)
    return {
        "roles": {str(row.unit_role_id): row.unit_role_name for row in role_types},
        "mastery": dict(mastery),
        "universal": {str(k): v for k, v in UNIVERSAL_MASTERY_ITEMS.items()},
        "costs": costs or DEFAULT_MASTERY_COSTS,
    }


def build_mastery_payload(client, alias: str) -> Dict[str, Any]:
    from ..db.database import db

    metadata = _mastery_metadata()
    relevant_items = set(UNIVERSAL_MASTERY_ITEMS.values())
    for role in metadata["mastery"].values():
        for slot in role.values():
            relevant_items.update(slot["items"].values())

    role_states = []
    for role in client.data.unit_role_list or []:
        role_states.append({
            "unit_role_id": role.unit_role_id,
            **{
                f"{kind}_{slot}": getattr(role, f"{kind}_{slot}")
                for slot in range(1, 5)
                for kind in ("slot_level", "enhance_level")
            },
        })

    stocks = {
        str(item_id): client.data.get_inventory((eInventoryType.Item, item_id))
        for item_id in sorted(relevant_items)
    }
    return {
        "account": alias,
        "data_time": db.format_time(datetime.fromtimestamp(client.data.data_time)),
        "metadata": metadata,
        "unit_role_list": role_states,
        "stocks": stocks,
    }
