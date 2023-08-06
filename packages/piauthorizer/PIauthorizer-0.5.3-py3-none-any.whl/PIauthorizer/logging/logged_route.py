import logging
import time
import traceback
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from fastapi.security.utils import get_authorization_scheme_param
from PIauthorizer.authorization import decode_token

route_logger = logging.getLogger("RouteLogger")
route_logger.addHandler(logging.NullHandler())

class LoggedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start_time = time.perf_counter()
            
            response: Response = await original_route_handler(request)
            
            finish_time = time.perf_counter()
            execution_time = finish_time - start_time
            
            overall_status = "successful" if response.status_code < 400 else "failed"
            tenant_name = "N/A"
            external_id = "N/A"
            
            # Obtain the tenant name if they have been authenticated.
            auth_header = request.headers.get("Authorization", None)
            if(auth_header):
                scheme, param = get_authorization_scheme_param(auth_header)
                if scheme.lower() != "bearer":
                    raise Exception("Authentication scheme is not using bearer token.")
                
                try:
                    decoded_token = decode_token(param)
                except Exception:
                    traceback.print_exc()
                    raise Exception("Unable to decode token.")
                    
                tenant_name = decoded_token.get('tenantname', tenant_name)
                
            # Obtain the external ID from the request body if available.
            if await request.body():
                body = await request.json()
                
                external_id = body.get('ExternalID', external_id)

            route_logger.info(f"Request {overall_status}, {request.method} {request.url.path}, "
                              f"status code={response.status_code}, tenant={tenant_name}, "
                              f"externalID={external_id} took={execution_time:0.4f}s")
            
            return response

        return custom_route_handler
