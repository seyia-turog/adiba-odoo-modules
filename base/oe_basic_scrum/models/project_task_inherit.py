from odoo import models, fields, api


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    x_sprint_id = fields.Many2one(comodel_name="sprint.task", string="Sprint", required=False)
    x_release_id = fields.Many2one(comodel_name="sprint.release", string="Release", required=False, store=True)
    x_user_story_id = fields.Many2one(comodel_name="sprint.user.story", string="User Story", required=False, )

