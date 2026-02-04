#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fetchez.core
~~~~~~~~~~~~~

Preset 'hook' macros.

:copyright: (c) 2010-2026 Regents of the University of Colorado
:license: MIT, see LICENSE for more details.
"""

import os
import json
import logging

# example presets.json
# {
#   "presets": {
#     "archive-ready": {
#       "help": "Checksum, Enrich, Audit, and save to archive.log",
#       "hooks": [
#         {"name": "checksum", "args": {"algo": "sha256"}},
#         {"name": "enrich"},
#         {"name": "audit", "args": {"file": "archive_log.json"}}
#       ]
#     },
# }

home_dir = os.path.expanduser('~')
CONFIG_PATH = os.path.join(home_dir, '.fetchez', 'presets.json')

logger = logging.getLogger(__name__)    

def load_user_presets():
    """Load presets from the user's config file."""
    
    if not os.path.exists(CONFIG_PATH):
        return {}
        
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            return data.get('presets', {})
    except Exception as e:
        logger.warning(f'Could not load presets: {e}') 
        return {}

    
def hook_list_from_preset(preset_def):
    """Convert JSON definition to list of Hook Objects."""
    
    from fetchez.hooks.registry import HookRegistry
    
    hooks = []
    for h_def in preset_def.get('hooks', []):
        name = h_def.get('name')
        kwargs = h_def.get('args', {})
        
        # Instantiate using the Registry
        hook_cls = HookRegistry.get_hook(name)
        if hook_cls:
            hooks.append(hook_cls(**kwargs))
            
    return hooks
