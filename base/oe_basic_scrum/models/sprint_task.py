from odoo import _, models, fields, api


class SprintTask(models.Model):
    _name = 'sprint.task'
    _rec_name = 'x_name'
    _description = 'Sprint Task'

    x_name = fields.Char(string="Name", required=False)
    x_sprint_objective = fields.Text(string="Object", required=False, )
    x_status = fields.Selection(string="Status",
                                selection=[('to_do', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')],
                                required=False, default="to_do")
    x_sprint_release_id = fields.Many2one(comodel_name="sprint.release", string="Sprint Release")
    x_project_id = fields.Many2one(comodel_name="project.project", string="Project", required=True)
    x_task_ids = fields.One2many(comodel_name="project.task", inverse_name="x_sprint_id", string="Tasks",
                                 required=False)
    x_task_text = fields.Text(string="Tasks", required=False, compute="_compute_task")
    x_user_story_ids = fields.One2many(comodel_name="sprint.user.story", inverse_name="x_sprint_id",
                                       string="User Story", required=False, )
    x_sprint_review = fields.Text(string="Sprint Review", required=False)
    x_task_to_improve_ids = fields.Many2many(comodel_name="project.task", string="Tasks To Improve")
    x_retrospective = fields.Text(string="Retrospective", required=False)
    x_start_date = fields.Date(string="Start Date", required=False)
    x_end_date = fields.Date(string="End Date", required=False)

    @api.model
    def create(self, values):
        project_id = values['x_project_id']
        if project_id:
            code = str(project_id) + '.project.sprint'
        values['x_name'] = self.env["ir.sequence"].next_by_code(code) or _('New')
        return super(SprintTask, self).create(values)

    @api.depends('x_task_ids')
    def _compute_task(self):
        for record in self:
            task_text = ""
            for task in record.x_task_ids:
                task_text = task_text + task.name + "<br/>"
            if task_text == "":
                task_text = "No task created yet"
            record['x_task_text'] = task_text

    def open_story(self):
        action = self.env.ref('oe_basic_scrum.win_action_user_story').read()[0]
        action['domain'] = [('x_project_id', '=', self.x_project_id.id),
                            ('x_sprint_release_id', '=', self.x_sprint_release_id.id),
                            ('x_sprint_id', '=', self.id)]
        action['context'] = {
            'default_x_project_id': self.x_project_id.id,
            'default_x_sprint_release_id': self.x_sprint_release_id.id,
            'default_x_sprint_id': self.id
        }
        return action

    def open_task(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]
        action['domain'] = [('project_id', '=', self.x_project_id.id), ('x_sprint_id', '=', self.id)]
        action['context'] = {
            'default_project_id': self.x_project_id.id,
            'default_x_sprint_id': self.id
        }
        return action
