import pytest

from ..options import Options


def test_options_defaults():
    class Meta:
        overwritten = True
        accepted = True

    options = Options(Meta, attr=True, overwritten=False)
    options.valid_attrs = ['accepted', 'overwritten']
    options.validate_attrs()

    assert options.attr
    assert options.overwritten


def test_options_contribute_to_class():
    class Meta:
        overwritten = True
        accepted = True

    class MyObject(object):
        pass

    options = Options(Meta, attr=True, overwritten=False)
    options.valid_attrs = ['accepted', 'overwritten']
    assert options.attr
    assert not options.overwritten
    options.contribute_to_class(MyObject, '_meta')
    assert MyObject._meta == options
    assert options.parent == MyObject


def test_options_invalid_attrs():
    class Meta:
        invalid = True

    class MyObject(object):
        pass

    options = Options(Meta, valid=True)
    options.valid_attrs = ['valid']
    assert options.valid
    with pytest.raises(TypeError) as excinfo:
        options.contribute_to_class(MyObject, '_meta')

    assert "MyObject.Meta got invalid attributes: invalid" == str(excinfo.value)