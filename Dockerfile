FROM python:3.9-alpine

ARG STACOSYS_VERSION=2.0
ARG STACOSYS_FILENAME=stacosys-${STACOSYS_VERSION}-py3-none-any.whl

RUN apk update && apk add bash && apk add wget && rm -rf /var/cache/apk/* 

COPY docker/docker-init.sh /usr/local/bin/
RUN chmod +x usr/local/bin/docker-init.sh

RUN cd /
#COPY ${STACOSYS_FILENAME} /
RUN wget https://github.com/kianby/stacosys/releases/download/${STACOSYS_VERSION}/${STACOSYS_FILENAME}
RUN python3 -m pip install ${STACOSYS_FILENAME} --target /stacosys
RUN rm -f ${STACOSYS_FILENAME}

WORKDIR /stacosys
CMD ["docker-init.sh"]
