# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
from odoo import _
from odoo.exceptions import MissingError
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.component.core import Component
from odoo.http import request


class ProductImageService(Component):
    _inherit = "base.rest.service"
    _name = "product_image.service"
    _usage = "product_image"
    _collection = "base.rest.public.services"
    _description = """
Product Image Services

Service used to retrieve the product's image
    """

    @skip_secure_response
    def get(self, _id, size):
        """
        Get product's informations
        """
        field = "image"
        if size == "small":
            field = "image_small"
        elif size == "medium":
            field = "image_medium"
        status, headers, content = self.env["ir.http"].binary_content(
            model="product.product", id=_id, field=field, env=self.env
        )
        if not content:
            raise MissingError(_("No image found for partner %s") % _id)
        image_base64 = base64.b64decode(content)
        headers.append(("Content-Length", len(image_base64)))
        response = request.make_response(image_base64, headers)
        response.status_code = status
        return response

    # Validator
    def _validator_get(self):
        return {
            "size": {
                "type": "string",
                "required": False,
                "default": "small",
                "allowed": ["small", "medium", "large"],
            }
        }
