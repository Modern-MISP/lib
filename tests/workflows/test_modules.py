from mmisp.workflows.modules import ModuleConfiguration, ModuleParam, ModuleParamType


def test_extraneous_keys() -> None:
    cfg = ModuleConfiguration(data={"foo": "bar"})

    errors = cfg.validate({})

    assert len(errors) == 1
    assert "Unspecified keys found in configuration: {'foo'}" in errors


def test_missing_key() -> None:
    cfg = ModuleConfiguration(data={})
    errors = cfg.validate({"foo": ModuleParam("foo", "Foo", ModuleParamType.INPUT, {})})

    assert len(errors) == 1
    assert "Missing configured key foo" in errors


def test_errors() -> None:
    cfg = ModuleConfiguration(data={"foo": 1, "bar": 2, "baz": 3, "fizzbuzz": True})
    errors = cfg.validate(
        {
            "foo": ModuleParam("foo", "Foo", ModuleParamType.CHECKBOX, {}),
            "bar": ModuleParam("bar", "Bar", ModuleParamType.PICKER, {"a": "b"}),
            "baz": ModuleParam("baz", "Baz", ModuleParamType.SELECT, {"a": "b"}),
            "fizzbuzz": ModuleParam("fizzbuzz", "Fizz Buzz", ModuleParamType.CHECKBOX, {}),
        }
    )

    assert len(errors) == 3

    assert "Param bar has an invalid value" in errors
    assert "Param baz has an invalid value" in errors
    assert "Param foo is expected to be a boolean" in errors
