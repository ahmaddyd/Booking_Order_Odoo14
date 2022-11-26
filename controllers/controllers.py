# -*- coding: utf-8 -*-
# from odoo import http


# class BookingOrderAhmadyd(http.Controller):
#     @http.route('/booking_order_ahmadyd/booking_order_ahmadyd/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_ahmadyd/booking_order_ahmadyd/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_ahmadyd.listing', {
#             'root': '/booking_order_ahmadyd/booking_order_ahmadyd',
#             'objects': http.request.env['booking_order_ahmadyd.booking_order_ahmadyd'].search([]),
#         })

#     @http.route('/booking_order_ahmadyd/booking_order_ahmadyd/objects/<model("booking_order_ahmadyd.booking_order_ahmadyd"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_ahmadyd.object', {
#             'object': obj
#         })
