from odoo import models, fields, api


class SprintRelease(models.Model):
    _name = 'sprint.release'
    _rec_name = 'x_name'
    _description = 'Sprint Release'

    x_name = fields.Char("Name", required=True)
    x_number_of_sprint = fields.Integer(string="Number of Sprint", required=False, compute="_compute_number_of_sprint")
    x_sprint_start_date = fields.Date(string="Start Date", required=False)
    x_sprint_end_date = fields.Date(string="End Date", required=False, )
    x_project_id = fields.Many2one(comodel_name="project.project", string="Project", required=True)
    x_sprint_ids = fields.One2many(comodel_name="sprint.task", inverse_name="x_sprint_release_id", string="Sprints",
                                   required=False)
    x_sprint_text = fields.Text(string="Sprint Text", required=False, compute="_compute_sprint_text")
    x_count_sprint = fields.Integer(string="Count Sprint", required=False, compute="_count_sprint")
    x_status = fields.Selection(string="Status",
                                selection=[('to_do', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')],
                                required=False, default="to_do", store=True)
    x_sprint_objective = fields.Text(string="Objective", required=False, )
    x_user_story_ids = fields.One2many(comodel_name="sprint.user.story", inverse_name="x_sprint_release_id",
                                       string="User Story", required=False)
    x_task_ids = fields.One2many(comodel_name="project.task", inverse_name="x_release_id",
                                 string="Tasks", required=False, )

    @api.depends('x_sprint_ids')
    def _compute_number_of_sprint(self):
        for record in self:
            record['x_number_of_sprint'] = len(record.x_sprint_ids)

    @api.model
    def create(self, values):
        result = super(SprintRelease, self).create(values)
        for i in range(result.x_number_of_sprint):
            self.env['sprint.task'].create({
                'x_name': 'Sprint ' + str(i + 1),
                'x_project_id': result.x_project_id.id,
                'x_sprint_release_id': result.id
            })
        return result

    @api.depends('x_sprint_ids')
    def _compute_sprint_text(self):
        for record in self:
            sprint_text = ""
            for sprint in record.x_sprint_ids:
                sprint_text = sprint_text + sprint.x_name + "(" + str(
                    sprint.x_status) + ")<br/>"
            if sprint_text == "":
                sprint_text = "No sprints created yet"
            record['x_sprint_text'] = sprint_text

    @api.depends('x_count_sprint')
    def _compute_amount(self):
        for record in self:
            record['x_count_sprint'] = len(record.x_sprint_ids)

    def open_win_action_sprint(self):
        action = self.env.ref('oe_basic_scrum.win_action_sprint_task').read()[0]
        action['domain'] = [('x_sprint_release_id', '=', self.id)]
        action['name'] = self.x_name
        action['context'] = {
            'default_x_sprint_release_id': self.id
        }
        return action

    def open_win_action_task(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]
        action['domain'] = [('x_release_id', '=', self.id)]
        action['context'] = {
            'default_x_release_id': self.id
        }
        return action

    def open_story(self):
        action = self.env.ref('oe_basic_scrum.win_action_user_story').read()[0]
        action['domain'] = [('x_project_id', '=', self.x_project_id.id), ('x_sprint_release_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.x_project_id.id,
            'default_x_sprint_release_id': self.id
        }
        return action
