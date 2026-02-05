from tyni_fish.agent import AgentRunner


def test_math_smoke():
    runner = AgentRunner.from_config(provider_name="dummy")
    out = runner.run("2+2")
    assert "4" in out


def test_note_and_read():
    runner = AgentRunner.from_config(provider_name="dummy")
    out1 = runner.run("write note: test-line")
    assert "ok" in out1
    out2 = runner.run("read notes")
    assert "test-line" in out2
