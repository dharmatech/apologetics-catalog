from typing import Any

from pydantic import BaseModel, ConfigDict


class EntityRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    kind: str
    section: str
    data: dict[str, Any]
    file: str
    line: int | None = None
    column: int | None = None


class Catalog(BaseModel):
    model_config = ConfigDict(frozen=True)

    entities: dict[str, EntityRecord]
    relationships: tuple[EntityRecord, ...]

    def get(self, entity_id: str) -> EntityRecord | None:
        return self.entities.get(entity_id)

    def relationships_from(self, entity_id: str) -> list[EntityRecord]:
        return [
            relationship
            for relationship in self.relationships
            if relationship.data.get("from_id") == entity_id
        ]

    def relationships_to(self, entity_id: str) -> list[EntityRecord]:
        return [
            relationship
            for relationship in self.relationships
            if relationship.data.get("to_id") == entity_id
        ]

    def references_to(self, entity_id: str) -> list[EntityRecord]:
        return [
            entity
            for entity in self.entities.values()
            if _record_references_id(entity.data, entity_id)
        ]

    def suggestions(self, query: str, *, limit: int = 10) -> list[str]:
        ids = sorted(self.entities)
        prefix_matches = [entity_id for entity_id in ids if entity_id.startswith(query)]
        substring_matches = [
            entity_id
            for entity_id in ids
            if query in entity_id and entity_id not in prefix_matches
        ]
        return [*prefix_matches, *substring_matches][:limit]


def _record_references_id(value: Any, entity_id: str) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if key != "id" and isinstance(key, str) and key.endswith("_id"):
                if item == entity_id:
                    return True
            if key != "id" and isinstance(key, str) and key.endswith("_ids"):
                if isinstance(item, list) and entity_id in item:
                    return True
            if key in {"holder", "attributed_to"} and isinstance(item, dict):
                if item.get("id") == entity_id:
                    return True
            if _record_references_id(item, entity_id):
                return True
        return False

    if isinstance(value, list):
        return any(_record_references_id(item, entity_id) for item in value)

    return False
