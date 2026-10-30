#!/bin/sh
if [ "$DEBUG_ENTRYPOINT" = "true" ]; then
    # Check if a custom command is provided for debugging; fall back to tailing /dev/null
    DEBUG_COMMAND=${DEBUG_COMMAND:-"tail -f /dev/null"}
    exec ${DEBUG_COMMAND}
else
    exec app-name
fi
