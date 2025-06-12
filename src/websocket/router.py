class WebSocketRouter:
    """Routes websocket connections to appropriate handlers."""
    def __init__(self, connection_manager, handler):
        self.connection_manager = connection_manager
        self.handler = handler

    def route(self, websocket):
        """Route the websocket connection to the handler."""
        pass 