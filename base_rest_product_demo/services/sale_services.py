# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component

from odoo.addons.base_rest.components.service import to_int, to_bool


class SaleService(Component):
    _inherit = "base.rest.service"
    _name = "sale.service"
    _usage = "sale"
    _collection = "base.rest.public.services"
    _description = """
Sale Order Services

A set of services allowing you to manage sales from external systems
    """

    def get(self, _id):
        """
        Get sale's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh sale by name
        """
        sales = self.env["sale.sale"].name_search(name)
        sales = self.env["sale.sale"].browse([i[0] for i in sales])
        rows = []
        res = {"count": len(sales), "rows": rows}
        for sale in sales:
            rows.append(self._to_json(sale))
        return res

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new sale
        """
        sale = self.env["sale.sale"].create(self._prepare_params(params))
        return self._to_json(sale)

    def update(self, _id, **params):
        """
        Update sale informations
        """
        sale = self._get(_id)
        sale.write(self._prepare_params(params))
        return self._to_json(sale)

    def archive(self, _id, **params):
        """
        Archive the given sale. This method is an empty method, IOW it
        don't update the sale. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        :param _id:
        :param params:
        :return:
        """
        return {"response": "Method archive called with id %s" % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["sale.sale"].browse(_id)

    def _prepare_params(self, params):
        for key in ["country", "state"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update(
            {"id": {"type": "integer", "required": True, "empty": False}}
        )
        return res

    def _validator_search(self):
        return {
            "name": {"type": "string", "nullable": False, "required": True}
        }

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {
                    "type": "dict",
                    "schema": self._validator_return_get(),
                },
            },
        }

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "street": {"type": "string", "required": True, "empty": False},
            "street2": {"type": "string", "nullable": True},
            "zip": {"type": "string", "required": True, "empty": False},
            "city": {"type": "string", "required": True, "empty": False},
            "phone": {"type": "string", "nullable": True, "empty": False},
            "state": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "nullable": True,
                    },
                    "name": {"type": "string"},
                },
            },
            "country": {
                "type": "dict",
                "schema": {
                    "id": {
                        "type": "integer",
                        "coerce": to_int,
                        "required": True,
                        "nullable": False,
                    },
                    "name": {"type": "string"},
                },
            },
            "is_company": {"coerce": to_bool, "type": "boolean"},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, sale):
        res = {
            "id": sale.id,
            "name": sale.name,
            "street": sale.street,
            "street2": sale.street2 or "",
            "zip": sale.zip,
            "city": sale.city,
            "phone": sale.city,
        }
        if sale.country_id:
            res["country"] = {
                "id": sale.country_id.id,
                "name": sale.country_id.name,
            }
        if sale.state_id:
            res["state"] = {"id": sale.state_id.id, "name": sale.state_id.name}
        return res
