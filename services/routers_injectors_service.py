from api_interface import security_system_api, state_check_update_api

routers = [
    security_system_api.api_router,
    state_check_update_api.api_router
]