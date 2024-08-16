from odoo import _, models, fields, api


class SprintUserStory(models.Model):
    _name = 'sprint.user.story'
    _rec_name = "x_story_id"
    _description = 'UserStory'

    x_story_id = fields.Char('Story ID')
    x_user_story = fields.Text(string="User Story", required=True)
    x_estimate_hour = fields.Float(string="Estimate Hour", required=False)
    x_priority = fields.Selection(string="Priority", selection=[('0', 'Low'), ('1', 'Medium'), ('2', 'High')],
                                  required=False, default=0)
    x_sprint_id = fields.Many2one(comodel_name="sprint.task", string="Sprint", store=True)
    x_sprint_release_id = fields.Many2one(comodel_name="sprint.release", string="Release", store=True)
    x_project_id = fields.Many2one(comodel_name="project.project", string="Project", store=True)
    x_task_ids = fields.One2many(comodel_name="project.task", inverse_name="x_user_story_id", string="Task",
                                 required=False, )

    @api.model
    def create(self, values):
        project_id = values['x_project_id']
        if project_id:
            code = str(project_id) + '.project.user.story'
        values['x_story_id'] = self.env["ir.sequence"].next_by_code(code) or _('New')
        return super(SprintUserStory, self).create(values)

    def open_task(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]
        action['domain'] = [('x_release_id', '=', self.x_sprint_release_id.id),
                            ('x_sprint_id', '=', self.x_sprint_id.id), ('x_user_story_id', '=', self.id)]
        action['context'] = {
            'default_x_user_story_id': self.id,
            'default_x_release_id': self.x_sprint_release_id.id,
            'default_x_sprint_id': self.x_sprint_id.id
        }
        return action

