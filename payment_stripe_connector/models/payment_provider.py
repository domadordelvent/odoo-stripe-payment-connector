# payment_stripe_connector/models/payment_provider.py

from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    stripe_connector_reference = fields.Char(
        string="Stripe Connector Reference",
        help="Internal reference used by the custom Stripe connector.",
    )
