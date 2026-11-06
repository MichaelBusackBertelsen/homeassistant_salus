"""Validate the HA 2026.11 conditional form with existing saved input keys."""

from copy import deepcopy
from pathlib import Path

import pytest
from homeassistant.components.automation.config import AUTOMATION_BLUEPRINT_SCHEMA
from homeassistant.components.blueprint.models import Blueprint, BlueprintInputs
from homeassistant.const import __version__
from homeassistant.core import HomeAssistant
from homeassistant.util import yaml as yaml_util

pytestmark = pytest.mark.skipif(
    tuple(map(int, __version__.split(".")[:2])) < (2026, 11),
    reason="Conditional blueprint visibility requires HA 2026.11",
)


@pytest.mark.parametrize("enabled", [False, True])
async def test_saved_room_limits_resolve_with_conditional_form(tmp_path, enabled):
    """Honor saved limits when enabled and use ignored defaults when hidden."""
    hass = HomeAssistant(str(tmp_path))
    try:
        path = (
            Path(__file__).resolve().parents[1]
            / "blueprints/automation/salus_comfort_rule.yaml"
        )
        raw = yaml_util.load_yaml_dict(str(path))
        bp = Blueprint(
            deepcopy(raw),
            expected_domain="automation",
            schema=AUTOMATION_BLUEPRINT_SCHEMA,
        )
        instance = BlueprintInputs(
            bp,
            {
                "use_blueprint": {
                    "path": str(path),
                    "input": {
                        "source": "weather.test",
                        "floor_entities": ["select.example"],
                        "use_room_minimum": enabled,
                        "room_minimum": 20,
                        "room_margin": 0.7,
                        "use_room_maximum": enabled,
                        "room_maximum": 24,
                    },
                }
            },
        )
        instance.validate()
        config = instance.async_substitute()
        data = config.get("actions", config.get("action"))[0]["data"]
        assert data["use_room_minimum"] is enabled
        assert data["use_room_maximum"] is enabled
        assert data["room_minimum"] == (20 if enabled else 21)
        assert data["room_margin"] == (0.7 if enabled else 0.5)
        assert data["room_maximum"] == (24 if enabled else 25)
    finally:
        await hass.async_stop()


async def test_in_place_update_keeps_saved_keys_defaults_and_control_flow(tmp_path):
    """Re-import requires no new automation, renamed inputs or changed service calls."""
    hass = HomeAssistant(str(tmp_path))
    try:
        root = Path(__file__).resolve().parents[1] / "blueprints/automation"
        current = yaml_util.load_yaml_dict(str(root / "salus_comfort_rule.yaml"))
        legacy = yaml_util.load_yaml_dict(str(root / "salus_comfort_rule_legacy.yaml"))
        current_meta = current.pop("blueprint")
        legacy_meta = legacy.pop("blueprint")
        assert current == legacy
        for section, metadata in current_meta["input"].items():
            assert (
                metadata["input"].keys()
                == legacy_meta["input"][section]["input"].keys()
            )
            for key, item in metadata["input"].items():
                old_item = legacy_meta["input"][section]["input"][key]
                assert {k: v for k, v in item.items() if k != "visible"} == old_item
        assert current_meta["source_url"].endswith("/salus_comfort_rule.yaml")
    finally:
        await hass.async_stop()
