from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #ofbool
    is_booking_order = fields.Boolean(string='Is Booking Order')
    
    #ofm20
    team = fields.Many2one(comodel_name='service.team', string='Team')
    team_leader = fields.Many2one(comodel_name='res.users', string='Team Leader')

    #ofm2m
    team_members = fields.Many2many(comodel_name='res.users', string='Team Members')
        
    #ofdatetime
    booking_start = fields.Datetime(string='Booking Start')
    booking_end = fields.Datetime(string='Booking End')

    #oofcompute
    wo_count = fields.Integer(
        string='Work Order',
        compute='_compute_wo_count')
    def _compute_wo_count(self):
        wo_data = self.env['work.order'].sudo().read_group([('booking_order_reference', 'in', self.ids)], ['booking_order_reference'],
                                                                   ['booking_order_reference'])
        
        result = {
            data['booking_order_reference'][0]: data['booking_order_reference_count'] for data in wo_data
        }

        for wo in self:
            wo.wo_count = result.get(wo.id, 0)

    @api.onchange('team')
    def _onchange_team(self):
        search = self.env['service.team'].search([('id', '=', self.team.id)])
        
        team_members = []
        
        for team in search:
            team_members.extend(members.id for members in team.team_members)
            self.team_leader = team.team_leader.id
            self.team_members = team_members

    def action_check(self):
        for check in self:
            wo = self.env['work.order'].search(
                ['|', '|', '|',
                 ('team_leader', 'in', [g.id for g in self.team_members]),
                 ('team_members', 'in', [self.team_leader.id]),
                 ('team_leader', '=', self.team_leader.id),
                 ('team_members', 'in', [g.id for g in self.team_members]),
                 ('state', '!=', 'cancelled'),
                 ('planned_start', '<=', self.booking_end),
                 ('planned_end', '>=', self.booking_start)], limit=1)
            
            if wo:
                raise ValidationError('Team already has work order during that period on SOXX')
            else:
                raise ValidationError('Team is available for booking')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
        for order in self:
            wo = self.env['work.order'].search(
                ['|', '|', '|',
                 ('team_leader', 'in', [g.id for g in self.team_members]),
                 ('team_members', 'in', [self.team_leader.id]),
                 ('team_leader', '=', self.team_leader.id),
                 ('team_members', 'in', [g.id for g in self.team_members]),
                 ('state', '!=', 'cancelled'),
                 ('planned_start', '<=', self.booking_end),
                 ('planned_end', '>=', self.booking_start)], limit=1)
            
            if wo:
                raise ValidationError('Team is not available during this period, already booked on '
                                      'SOXX. Please book on another date.')
            order.action_work_order_create()
        
        return res

    def action_work_order_create(self):
        wo_obj = self.env['work.order']
        
        for order in self:
            wo_obj.create([{'booking_order_reference': order.id,
                            'team': order.team.id,
                            'team_leader': order.team_leader.id,
                            'team_members': order.team_members.ids,
                            'planned_start': order.booking_start,
                            'planned_end': order.booking_end}])