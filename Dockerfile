FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
# Creating working directory
RUN mkdir /fampay_assignment
WORKDIR /fampay_assignment
# Copying requirements
COPY . .
COPY background.conf /etc/supervisor/
RUN apk --update add supervisor && pip install -r requirements.txt

RUN chmod +x init.sh

CMD ["./init.sh"]