SHELL=/bin/bash
INSTALL_DIR=${HOME}/bin/

install: ${INSTALL_DIR}/find-dead-links
${INSTALL_DIR}/find-dead-links: env
	echo "#!/bin/bash" > find-dead-links
	echo "source ${PWD}/env/bin/activate &&" >> find-dead-links
	echo "python ${PWD}/find-dead-links.py \$$@" >> find-dead-links
	chmod 755 find-dead-links
	cp find-dead-links ${INSTALL_DIR}

env: ${PWD}/env/
${PWD}/env/:
	virtualenv -p python3 env
	./env/bin/pip install requests
	./env/bin/pip install beautifulsoup4
