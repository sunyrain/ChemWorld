"""Observation adapter seam. No physical hardware driver is implemented here."""

import time
import uuid
from abc import ABC, abstractmethod


class DeviceAdapter(ABC):
    @abstractmethod
    def capabilities(self):
        """Describe the adapter and its implemented operations."""

    @abstractmethod
    def observations(self):
        """Yield normalized, timestamped observation envelopes."""

    def execute(self, command):
        raise NotImplementedError("Physical command dispatch is not configured")

    def stop(self):
        raise NotImplementedError("Physical stop driver is not configured")


class MockTemperatureAdapter(DeviceAdapter):
    def __init__(self, client, asset_id="reactor_01", offset=0):
        self.client = client
        self.asset_id = asset_id
        self.offset = offset
        self.binding_id = "mock_" + asset_id
        self.calibration_id = "mock-calibration-1"

    def capabilities(self):
        return {
            "adapter": "mock",
            "synthetic": True,
            "observations": ["temperature_c"],
            "hardware_dispatch": False,
        }

    def bind(self):
        return self.client.bind(
            binding_id=self.binding_id,
            asset_id=self.asset_id,
            physical_id="MOCK-" + self.asset_id,
            adapter="mock",
            calibration_id=self.calibration_id,
            max_age_s=15,
        )

    def observations(self):
        value = self.client.get(self.asset_id)["state"]["temperature_c"] + self.offset
        yield {
            "observation_id": "mock_obs_" + uuid.uuid4().hex,
            "binding_id": self.binding_id,
            "metric": "temperature_c",
            "value": value,
            "unit": "degC",
            "source_timestamp": time.time(),
            "sequence": time.time_ns(),
            "quality": "good",
            "calibration_id": self.calibration_id,
        }

    def publish_once(self):
        return [self.client.publish(**item) for item in self.observations()]


class UnconfiguredHardwareAdapter(DeviceAdapter):
    def __init__(self, protocol):
        if protocol not in {"sila2", "opcua", "ros2"}:
            raise ValueError("Unknown adapter protocol")
        self.protocol = protocol

    def capabilities(self):
        return {"adapter": self.protocol, "status": "not_implemented", "hardware_dispatch": False}

    def observations(self):
        raise NotImplementedError("Install and validate a device-specific driver first")
