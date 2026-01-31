# Copyright (C) 2025, CraftIQ.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

import os

import hwte

PROJECT_NAME: str = "hwte API template"
PROJECT_DESCRIPTION: str = "Template API for Optical Character Recognition"
VERSION: str = hwte.__version__
DEBUG: bool = os.environ.get("DEBUG", "") != "False"
