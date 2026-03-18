FROM python:3.9

# Set up the workspace
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project across and start
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
