from api_interface import db_update_api, security_system_api, state_check_update_api

routers = [
    security_system_api.api_router,
    state_check_update_api.api_router,
    db_update_api.api_router
]