#!/usr/bin/env python

"""Tests for `streamdeck_manager` package."""

import streamdeck_manager

def test_package_publishes_version_info():
    """Tests that the `streamdeck_manager` publishes the current verion"""

    assert hasattr(streamdeck_manager, '__version__')
