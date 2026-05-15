"""Small demo dataset used by the CLI and tests."""

from __future__ import annotations

from typing import Dict, List

from .models import AssetRecord, InventoryItem, TenantGuardrails


def demo_assets() -> Dict[str, AssetRecord]:
    return {
        "COMP-04": AssetRecord(
            asset_id="COMP-04",
            name="Air Compressor 04",
            class_code="ROTATING_COMPRESSOR",
            site_id="PLANT-01",
            criticality=4,
            status="operating",
            last_pm_days_ago=104,
            failure_modes=["bearing wear", "misalignment", "lubrication loss", "loose mounting"],
            safety_notes=["Lockout/tagout before guard removal", "Verify stored air pressure is released"],
        ),
        "PUMP-12": AssetRecord(
            asset_id="PUMP-12",
            name="Cooling Water Pump 12",
            class_code="CENTRIFUGAL_PUMP",
            site_id="PLANT-01",
            criticality=3,
            status="operating",
            last_pm_days_ago=45,
            failure_modes=["seal leak", "cavitation", "bearing wear"],
            safety_notes=["Confirm isolation valves before seal inspection"],
        ),
    }


def demo_inventory() -> List[InventoryItem]:
    return [
        InventoryItem(
            part_no="BRG-6205-2RS",
            description="Deep groove bearing for rotating compressor drive end",
            on_hand=2,
            reorder_point=2,
            lead_time_days=7,
            compatible_asset_classes=["ROTATING_COMPRESSOR", "CENTRIFUGAL_PUMP"],
        ),
        InventoryItem(
            part_no="LUBE-ISO46",
            description="ISO 46 compressor lubricant",
            on_hand=12,
            reorder_point=4,
            lead_time_days=2,
            compatible_asset_classes=["ROTATING_COMPRESSOR"],
        ),
        InventoryItem(
            part_no="CPL-FLEX-090",
            description="Flexible coupling 90 mm compressor shaft",
            on_hand=1,
            reorder_point=1,
            lead_time_days=14,
            compatible_asset_classes=["ROTATING_COMPRESSOR"],
        ),
    ]


def demo_guardrails() -> TenantGuardrails:
    return TenantGuardrails(
        tenant_id="demo-tenant",
        budget_cap_cents=200,
        max_tool_calls=5,
        human_approval_gate=True,
        allow_live_writes=False,
        high_risk_threshold=0.65,
        low_confidence_threshold=0.72,
    )
