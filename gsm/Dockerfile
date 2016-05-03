FROM  ubuntu:14.04

RUN apt-get -y install wget && \
    echo deb http://dev.monetdb.org/downloads/deb/ trusty monetdb >  /etc/apt/sources.list.d/monetdb.list && \
    echo deb-src http://dev.monetdb.org/downloads/deb/ trusty monetdb >>  /etc/apt/sources.list.d/monetdb.list && \
    wget --output-document=- https://www.monetdb.org/downloads/MonetDB-GPG-KEY | sudo apt-key add - && \
    apt-get -y update && \
    apt-get -y install monetdb5-sql monetdb-client && \
    useradd -m monet && \
    usermod -a -G monetdb monet

USER monet

RUN echo user=monetdb > ${HOME}/.monetdb && \
    echo password=monetdb >> ${HOME}/.monetdb && \
    monetdbd create ${HOME}/monetdb-lofar-farm && \
    monetdbd start ${HOME}/monetdb-lofar-farm && monetdb create gsm && \
    monetdb release gsm && \
    mclient -d gsm -s "CREATE user gsm WITH PASSWORD 'msss' NAME 'GlobalSkyModel2' SCHEMA sys" && \
    mclient -d gsm -s 'CREATE SCHEMA "gsm" AUTHORIZATION "gsm"' && \
    mclient -d gsm -s 'ALTER USER "gsm" SET SCHEMA "gsm"' && \
    monetdbd set port=51000 ${HOME}/monetdb-lofar-farm 

COPY ./gsm.sql.bz2 /home/monet/gsm.sql.bz2

RUN cd /home/monet/ && bunzip2 /home/monet/gsm.sql.bz2 && \
    echo user=gsm > ${HOME}/.monetdb && \
    echo password=msss >> ${HOME}/.monetdb && \
    monetdbd start ${HOME}/monetdb-lofar-farm && monetdb start gsm && mclient -lsql -p 51000 --database=gsm ${HOME}/gsm.sql && \
    echo \#\! /usr/bin/env bash > ${HOME}/start_db_script && \
    echo monetdbd start ${HOME}/monetdb-lofar-farm >> ${HOME}/start_db_script && \
    echo monetdb start gsm >> ${HOME}/start_db_script && \
    echo tail -f ${HOME}/monetdb-lofar-farm/merovingian.log >> ${HOME}/start_db_script && \
    chmod 744 ${HOME}/start_db_script && \
    rm -f gsm.sql

# Installing the gsm client from lofar software
USER root
RUN apt-get -y install subversion make cmake python-dev liblog4cplus-dev python-pip g++ python-numpy && \
    pip install python-monetdb

USER monet
RUN mkdir -p ${HOME}/opt/lofar/build/gnu_opt && cd ${HOME}/opt/lofar && svn co -N https://svn.astron.nl/LOFAR/tags/LOFAR-Release-2_16_2/ src && \
    svn up src/CMake && cd build/gnu_opt && cmake ../../src cmake -DBUILD_PACKAGES="GSM" -DCMAKE_INSTALL_PREFIX=${HOME}/opt ../../src && \
    make && make install && rm -rf ${HOME}/opt/lofar/build ${HOME}/opt/lofar/src &&\
    echo "#!/usr/bin/env bash" > ${HOME}/gsm && \
    echo "${HOME}/start_db_script > /tmp/monetlog &" >> ${HOME}/gsm && \
    echo "source ${HOME}/opt/lofarinit.sh" >> ${HOME}/gsm && \
    echo "gsm.py ${HOME}/TMPFILE \$*" >> ${HOME}/gsm && \
    echo "cat ${HOME}/TMPFILE" >> ${HOME}/gsm && \
    chmod 744 ${HOME}/gsm


WORKDIR /home/monet

ENTRYPOINT ["/home/monet/gsm"]
