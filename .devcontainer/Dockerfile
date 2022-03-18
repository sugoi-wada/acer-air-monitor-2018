FROM ludeeus/container:integration-debian
RUN apt-get update && python3 -m pip install --upgrade pip
# HOTFIX: https://github.com/custom-components/integration_blueprint/issues/71
RUN { \
    echo '#!/bin/bash'; \
    echo ""; \
    echo "function UpdgradeHomeAssistantDev {" ; \
    echo "  python3 -m pip install --upgrade git+https://github.com/home-assistant/home-assistant.git@dev" ; \
    echo "}"; \
    echo; \
} > /usr/share/container/upgrade
