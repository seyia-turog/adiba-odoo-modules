from odoo import models, fields, api


class ScrumMeeting(models.Model):
    _name = 'scrum.meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'x_name'
    _description = 'Scrum Meeting'

    x_name = fields.Char('Meeting Title', required=True)
    x_attendee_ids = fields.Many2many(comodel_name="res.users", string="Attendees", required=True)
    x_attendee_text = fields.Text(string="Attendee Text", required=False, compute="_compute_attendee_ids")
    x_project_id = fields.Many2one(comodel_name="project.project", string="Project", required=True)
    x_sprint_release_id = fields.Many2one(comodel_name="sprint.release", string="Sprint Release", required=True)
    x_meeting_start_date = fields.Datetime(string="Start", required=True)
    x_duration = fields.Float(string="Duration", required=False)
    x_description = fields.Text(string="Description", required=False, )
    x_location = fields.Text(string="Location", required=False, )
    x_happen_during_meeting = fields.Text(string="What happened during the meeting?", required=False)
    x_was_done_last_meeting = fields.Text(string="What was done since the last meeting?", required=False)
    x_plan_until_next_meeting = fields.Text(string="What is planned until the next meeting?", required=False)
    x_something_blocking = fields.Text(string="What is the blocking points?", required=False)

    @api.depends('x_attendee_ids')
    def _compute_attendee_ids(self):
        for record in self:
            attendee_text = ""
            for attendee in record.x_attendee_ids:
                attendee_text = attendee_text + attendee.name + "<br/>"
            record['x_attendee_text'] = attendee_text

    def open_scrum_report(self):
        action = self.env.ref('oe_basic_scrum.win_action_tasks').read()[0]
        action['name'] = 'Project:' + str(self.x_project_id.name) + " Release:  " + str(self.x_sprint_release_id.x_name)
        action['domain'] = [('project_id', '=', self.x_project_id.id),
                            ('x_release_id', '=', self.x_sprint_release_id.id)]
        action['context'] = {
            'search_default_sprint': 1,
        }
        return action

