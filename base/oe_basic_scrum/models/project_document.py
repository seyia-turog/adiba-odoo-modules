from odoo import models, fields, api

class ProjectDocument(models.Model):
    _name = 'project.document'
    _rec_name = 'x_name'
    _description = 'Project Document'

    x_name = fields.Char(string="Document Title")
    x_project_id = fields.Many2one(comodel_name="project.project", string="Project", required=True)
    x_document_file = fields.Binary(string="Upload File")
