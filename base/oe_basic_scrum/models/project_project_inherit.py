from odoo import models, fields, api
from odoo.exceptions import UserError


class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    x_product_owner_id = fields.Many2one(comodel_name="res.partner", string="Product Owner", required=False)
    x_scrum_master_id = fields.Many2one(comodel_name="res.users", string="Scrum Master", required=False)
    x_scrum_team_id = fields.Many2one(comodel_name="scrum.team", string="Scrum Team", required=False)
    x_is_scrum_project = fields.Boolean(string="Is Scrum Project", default=False)
    x_release_ids = fields.One2many(comodel_name="sprint.release", inverse_name="x_project_id", string="Releases",
                                    required=False)
    x_sprint_ids = fields.One2many(comodel_name="sprint.task", inverse_name="x_project_id", string="Sprint",
                                   required=False)
    x_scrum_meeting_ids = fields.One2many(comodel_name="scrum.meeting", inverse_name="x_project_id",
                                          string="Scrum Meetings")
    x_project_document_ids = fields.One2many(comodel_name="project.document", inverse_name="x_project_id",
                                             string="Documents", required=False, )
    x_user_story_ids = fields.One2many(comodel_name="sprint.user.story", inverse_name="x_project_id",
                                       string="User Story", required=False, )

    x_count_release = fields.Integer(string="Count Release", required=False, compute="_count_release")

    @api.depends('x_release_ids')
    def _count_release(self):
        for record in self:
            record['x_count_release'] = len(record.x_release_ids)

    def add_sprint_release(self):
        raise UserError("Add Sprint Release Click")

    def add_sprint(self):
        raise UserError("Add Sprint Click")

    def add_user_story(self):
        raise UserError("Add User Story")

    def open_win_action_sprint_release(self):
        action = self.env.ref('oe_basic_scrum.win_action_sprint_release').read()[0]
        action['domain'] = [('x_project_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.id
        }
        return action

    def open_win_action_sprint(self):
        action = self.env.ref('oe_basic_scrum.win_action_sprint_task').read()[0]
        action['domain'] = [('x_project_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.id
        }
        return action

    def open_win_action_user_story(self):
        action = self.env.ref('oe_basic_scrum.win_action_user_story').read()[0]
        action['domain'] = [('x_project_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.id
        }
        return action

    def open_project_document(self):
        action = self.env.ref('oe_basic_scrum.win_action_project_document').read()[0]
        action['domain'] = [('x_project_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.id
        }
        return action

    def open_task(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]
        action['domain'] = [('project_id', '=', self.id)]
        action['context'] = {
            'default_project_id': self.id
        }
        return action

    def open_win_action_sprint_meeting(self):
        raise UserError("Sprint Meeting Smart Button Click")

    def _create_project_sprint_sequence(self, result):
        code = str(result.id) + ".project.sprint"
        self.env['ir.sequence'].create({
            'name': result.name,
            'code': code,
            'prefix': 'Sprint',
            'padding': 1
        })

    def _create_project_user_story_sequence(self, result):
        code = str(result.id) + ".project.user.story"
        self.env['ir.sequence'].create({
            'name': result.name,
            'code': code,
            'prefix': 'US',
            'padding': 4
        })

    @api.model
    def create(self, values):
        result = super(ProjectProjectInherit, self).create(values)
        self._create_project_sprint_sequence(result)
        self._create_project_user_story_sequence(result)
        return result
