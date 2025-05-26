from docnote import ClcNote


def test_clc_note():
    """ClcNote instances must be constructable as expected.
    This is about as close to a gimme as you can get.
    """
    assert ClcNote('Some doc note here')
