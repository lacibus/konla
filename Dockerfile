#   Dockerfile to build a KONLA application
#   Copyright (c) Minyi Lei 2022
#   Modified by Lacibus Ltd April 2022. Modifications (c) Lacibus Ltd.

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG=C.UTF-8
ENV TZ="Europe/London"


RUN apt update && \
	apt install -y poppler-utils python3 python3-pip supervisor npm redis nginx

COPY . /konla

RUN python3 -m pip install -r /konla/requirements.txt
RUN python3 -m spacy download en_core_web_trf

RUN mkdir -p /var/log/supervisor

WORKDIR /konla/src/frontend/vue-web-app
RUN npm install --save-dev
RUN npm run build
RUN cp -r /konla/src/frontend/vue-web-app/dist/* /var/www/html
RUN cp /konla/configs/refresh.html /var/www/html

RUN chmod 755 /konla && chown www-data.www-data -R /konla
RUN chmod 700 /konla/CERT && chown root.root -R /konla/CERT

COPY ./configs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./configs/nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/bin/supervisord"]

EXPOSE 443
