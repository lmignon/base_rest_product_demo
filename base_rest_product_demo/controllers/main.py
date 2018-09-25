# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.controllers import main


class BaseRestProductDemoPublicApiController(main.RestController):
    _root_path = "/rest_api/public/"
    _collection_name = "base.rest.public.services"
    _default_auth = "public"
