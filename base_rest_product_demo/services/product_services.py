# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class ProductService(Component):
    _inherit = "base.rest.service"
    _name = "product.service"
    _usage = "product"
    _collection = "base.rest.public.services"
    _description = """
Product Services

A set of services to manage products from external systems
    """

    def get(self, _id):
        """
        Get product's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name=None, product_type=None):
        """
        Searh product by name and product_type
        """
        domain = []
        if name:
            domain.append(("name", "ilike", name))
        if product_type:
            domain.append(("type", "=", product_type))
        products = self.env["product.product"].search(domain)
        rows = []
        res = {"count": len(products), "rows": rows}
        for product in products:
            rows.append(self._to_json(product))
        return res

    def create(self, **params):
        """
        Create a new product
        """
        product = self.env["product.product"].create(
            self._prepare_params(params)
        )
        return self._to_json(product)

    def update(self, _id, **params):
        """
        Update product informations
        """
        product = self._get(_id)
        product.write(self._prepare_params(params))
        return self._to_json(product)

    def delete(self, _id):
        """
        Delete product
        """
        product = self._get(_id)
        product.unlink()

    def archive(self, _id, **params):
        """
        Archive the given product. This method is an empty method, IOW it
        don't update the product. This method is part of the demo data to
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
        product = self.env["product.product"].browse(_id)
        return product

    def _prepare_params(self, params):
        vals = {}
        if params.get("name"):
            vals["name"] = params["name"]
        if params.get("price"):
            vals["list_price"] = params["price"]
        return vals

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update(
            {
                "id": {"type": "integer", "required": True, "empty": False},
                "name": {"type": "string", "required": True, "empty": False},
                "price": {"type": "float", "required": True, "empty": False},
                "product_type": {
                    "type": "string",
                    "required": True,
                    "allowed": ["consu", "service"],
                },
                "reference": {
                    "type": "string",
                    "required": False,
                    "empty": True,
                },
                "attributes": {
                    "type": "list",
                    "required": False,
                    "nullable": True,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {
                                "type": "string",
                                "required": True,
                                "empty": False,
                            },
                            "value": {
                                "type": "string",
                                "required": True,
                                "empty": False,
                            },
                            "extra_price": {
                                "type": "float",
                                "required": False,
                                "empty": True,
                            },
                        },
                    },
                },
            }
        )
        return res

    def _validator_search(self):
        return {
            "name": {"type": "string", "nullable": True, "required": False},
            "product_type": {
                "type": "string",
                "required": False,
                "allowed": ["consu", "service"],
            },
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
            "price": {"type": "float", "required": True, "empty": False},
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

    def _to_json(self, product):
        res = {
            "id": product.id,
            "name": product.name,
            "price": product.list_price,
            "product_type": product.type,
            "reference": product.default_code or "",
            "attributes": None,
        }
        if product.attribute_value_ids:
            attributes = []
            for attr in product.attribute_value_ids:
                attributes.append(
                    {
                        "name": attr.attribute_id.name,
                        "value": attr.name,
                        "extra_price": attr.price_extra,
                    }
                )
            res["attributes"] = attributes
        return res
