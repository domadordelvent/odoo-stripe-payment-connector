# payment_stripe_connector/__manifest__.py

{
    "name": "Stripe Payment Connector",
    "version": "18.0.1.0.0",
    "category": "Accounting/Payment Providers",
    "summary": "Stripe payment connector for Odoo",
    "author": "Jordi Prim",
    "license": "LGPL-3",
    "depends": [
        "payment",
        "payment_stripe",
        "account_payment",
    ],
    "data": [
	"security/ir.model.access.csv",
	"views/payment_provider_views.xml",
	"views/stripe_payment_views.xml",
],
    "installable": True,
    "application": False,
    "auto_install": False,
}
