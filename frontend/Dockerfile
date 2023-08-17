FROM node:14.17.0
WORKDIR /app
COPY frontend/. .

RUN npm install --legacy-peer-deps
CMD ["npm", "run", "serve"]
