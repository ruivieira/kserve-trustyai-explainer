FROM python:3.7

COPY explainer explainer
COPY kserve kserve
COPY third_party third_party

# Install JDK
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2
RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-11-jre maven


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ./kserve && \
    pip install --no-cache-dir -e ./explainer

RUN pip install --no-cache-dir trustyai==0.2.4 --no-binary trustyai --force

EXPOSE 8080

RUN useradd kserve -m -u 1000 -d /home/kserve
USER 1000
ENTRYPOINT ["python", "-m", "trustyaiserver"]
