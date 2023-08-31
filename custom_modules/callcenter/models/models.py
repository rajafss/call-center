
from odoo import fields, models,api



class Callcenter(models.Model):

    _name = 'callcenter.callcenter'
    _inherit = ['mail.thread',
                'mail.activity.mixin']


    message_main_attachment_id = fields.Many2one(groupe= "callcenter.group_user")

    is_manager = fields.Boolean('is a manager',compute='_compute_is_manager')
    agent_id = fields.Many2one('res.users', required=True,
                               default=lambda self: self.env.user and self.env.user.id or False)
    name = fields.Char(string="Nom client", store = True)
    partner_id=fields.Many2one('reports.reports',string='Partner')
    phone = fields.Char(string= 'Numero Telephone' ,store = True)
    nom_voyant = fields.Char(string="Nom voyant")
    num_voyant = fields.Char(string="Numero Voyant")
    duree_appell = fields.Char(string = 'temps d\'un appel')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('to approve', 'waiting approval'),
            ('confirmed', 'Confirmed'),
            ('not confirmed', 'Not confirmed'),
            ],default='draft')
    description = fields.Text()
    qualification = fields.Selection([
        ('crm', 'CRM'),
        ('rappel', 'Rappel'),
        ('appel nauel', 'Appel manuel'),
        ('cb', 'CB')],store = True)
    # date = fields.datetime.now()

    @api.onchange('partner_id')
    def _onChage_partner_id(self, ):
        self.name = self.partner_id.name
        self.qualification = self.partner_id.qualification
        self.phone = self.partner_id.phone

    # compute is manager
    def _compute_is_manager(self):
        for rec in self:
            rec.is_manager= self.env.user.has_group('callcenter.group_manager')

    def draft_progressbar(self):
        self.write({
            'state': 'draft'

        })

    def to_approve_progressbar(self):
        self.write({
            'state': 'to approve',
        })

    # This function is triggered when the user clicks on the button 'Set to started'

    def confirmed_progressbar(self):
        self.write({
            'state': 'confirmed'
        })

    # This function is triggered when the user clicks on the button 'In progress'

    def not_confirmed_progressbar(self):
        self.write({
            'state': 'not confirmed'
        })

    @api.model
    def create(self, vals):
        partner_id = self.env['reports.reports'].search([('id', '=', vals['partner_id'])])
        if partner_id :
            qualification = partner_id.qualification
            vals['qualification'] = qualification

        print(vals)
        rec = super(Callcenter, self).create(vals)

        return rec

    def write(self, vals):
        print(vals)
        if 'qualification' in vals :
            if self.partner_id:
                vals['qualification'] = self.partner_id.qualification
        res = super(Callcenter, self).write(vals)

        return res
