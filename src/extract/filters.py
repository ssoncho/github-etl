from datetime import datetime, timezone

def filter_by_updated_at(items: list[dict], last_loaded_at: datetime | None) -> list[dict]:
    if last_loaded_at is None:
        return items

    if last_loaded_at.tzinfo is None:
        last_loaded_at = last_loaded_at.replace(tzinfo=timezone.utc)

    filtered_items = []
    for item in items:
        updated_at = item.get("updated_at")
        if not updated_at:
            filtered_items.append(item)
            continue

        try:
            updated_at_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError:
            filtered_items.append(item)
            continue

        if updated_at_dt >= last_loaded_at:
            filtered_items.append(item)

    return filtered_items