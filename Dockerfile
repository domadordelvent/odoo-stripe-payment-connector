FROM odoo:18

USER root

RUN pip3 install stripe --break-system-packages

USER odoo