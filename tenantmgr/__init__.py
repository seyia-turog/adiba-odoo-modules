# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo.exceptions import ValidationError



def _pre_init_conflict_check(cr):
    cr.execute("""
        SELECT id FROM ir_module_module
        WHERE name = 'adb-foundation'
        AND state = 'installed'
    """)
    module_installed = cr.fetchone()

    if module_installed:
        raise ValidationError('Digital banking module is not compatible with this module')
