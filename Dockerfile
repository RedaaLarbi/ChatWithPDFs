FROM  python:3.10
WORKDIR /frontend.py 
RUN pip install -r requirements.txt 
COPY . /frontend.py 
CMD python frontend.py 
