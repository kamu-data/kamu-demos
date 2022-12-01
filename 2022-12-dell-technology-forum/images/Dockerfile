FROM docker.io/kamudata/jupyter:0.5.0

#########################################################################################
USER root

RUN apt update \
    && apt -y install ffmpeg \
    && rm -rf /var/lib/apt/lists/*

#########################################################################################
USER $NB_USER

RUN pip --no-cache-dir install scipy

#########################################################################################
USER root
RUN chown -R $NB_USER:users /home/$NB_USER

USER $NB_USER
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "80", "--allow-root"]
