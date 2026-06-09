# models/stripe_payment.py

from odoo import fields, models
import stripe
import os
from odoo.exceptions import UserError


class StripePayment(models.Model):
    _name = "stripe.payment"
    _description = "Stripe Payment"

    name = fields.Char(required=True)
    amount = fields.Float(required=True)

    
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        default="draft",
    )


    partner_id = fields.Many2one(
	"res.partner",
	string="Customer",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    stripe_payment_intent_id = fields.Char(
        string="Stripe Payment Intent ID",
        readonly=True,
    )

    stripe_status = fields.Char(
        string="Stripe Status", 
        readonly=True,
        )
    
    stripe_client_secret = fields.Char(
        string="Stripe Client Secret",
        readonly=True,
    )

    def action_create_stripe_payment(self):
        
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        for payment in self:

            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency="eur",
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never",
                },
)

            payment.write({
                "state": "pending",
                "stripe_payment_intent_id": intent.id,
                "stripe_status": intent.status,
                "stripe_client_secret": intent.client_secret,
            })

    def action_check_stripe_status(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        for payment in self:
            if not payment.stripe_payment_intent_id:
                raise UserError("Create a Stripe Payment first.")

            intent = stripe.PaymentIntent.retrieve(
                payment.stripe_payment_intent_id
            )

            payment.write({
                "stripe_status": intent.status,
            })

    def action_mark_as_paid(self):
        for payment in self:
            payment.write({
                "state": "paid",
            })

    def action_mark_as_failed(self):
        for payment in self:
            payment.write({
                "state": "failed",
            })

    def action_confirm_test_payment(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        for payment in self:
            intent = stripe.PaymentIntent.retrieve(
                payment.stripe_payment_intent_id
            )

            if intent.status == "succeeded":
                payment.write({
                    "stripe_status": intent.status,
                    "state": "paid",
                })
                continue

            intent = stripe.PaymentIntent.confirm(
                payment.stripe_payment_intent_id,
                payment_method="pm_card_visa",
            )

            payment.write({
                "stripe_status": intent.status,
                "state": "paid" if intent.status == "succeeded" else "pending",
            })