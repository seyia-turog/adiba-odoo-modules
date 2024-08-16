from odoo import models, fields, api


class ScrumTeam(models.Model):
    _name = 'scrum.team'
    _rec_name = 'x_name'
    _description = 'Scrum Team'

    x_name = fields.Char(string="Team Name", required=True)
    x_member_ids = fields.Many2many(comodel_name="res.users", string="Members")
    x_member_text = fields.Text(string="Member Text", required=False, compute="_compute_member_id")

    @api.depends('x_member_ids')
    def _compute_member_id(self):
        for record in self:
            member_text = ""
            for member in record.x_member_ids:
                member_text = member_text + member.name + "<br/>"
            record['x_member_text'] = member_text
