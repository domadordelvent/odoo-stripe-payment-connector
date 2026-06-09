from odoo import http
from odoo.http import request


class StripeWebhookController(http.Controller):

    @http.route(
        "/stripe/webhook",
        type="json",
        auth="public",
        csrf=False,
        methods=["POST"],
    )
    def stripe_webhook(self, **kwargs):

        payload = request.get_json_data()

        event_type = payload.get("type")
        payment_intent = payload.get("data", {}).get("object", {})

        stripe_payment_intent_id = payment_intent.get("id")
        stripe_status = payment_intent.get("status")

        payment = request.env["stripe.payment"].sudo().search([
            ("stripe_payment_intent_id", "=", stripe_payment_intent_id)
        ], limit=1)

        if payment:
            if event_type == "payment_intent.succeeded":
                payment.write({
                    "state": "paid",
                    "stripe_status": stripe_status,
                })

            elif event_type == "payment_intent.payment_failed":
                payment.write({
                    "state": "failed",
                    "stripe_status": stripe_status,
                })