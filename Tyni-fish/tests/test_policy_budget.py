import pytest

from tyni_fish.agent import AgentRunner
from tyni_fish.policy import Policy


def test_max_steps_exceeded():
    # Force a provider that never returns final by using dummy with note loop? We'll simulate by low max_steps.
    runner = AgentRunner.from_config(provider_name="dummy")
    with pytest.raises(RuntimeError):
        runner.run("write note: a", max_steps=0)
