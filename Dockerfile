FROM python:3.9

WORKDIR /app
COPY . .

ENV db_name=dai5r9sal5lpok
ENV db_user=gjegxmrdprzlsa
ENV db_password=f842922283f1903599838a6b72fdca7d615066122f2c8009c30e4037ac7d2ebf
ENV db_host=ec2-54-195-246-55.eu-west-1.compute.amazonaws.com
ENV token=5235447854:AAHd1gpO-pDVQxP8frCutBEr3yx5bj9LFmw

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runbot"]