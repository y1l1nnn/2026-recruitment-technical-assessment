####### BUILD IMAGE #######
FROM node:20-slim AS build

# set working dir inside container 
WORKDIR /app        

# copy app files 
COPY package*.json ./

# install all dependencies 
RUN npm ci

# copy rest of source code
COPY . .

# compiles TS -> JS
RUN npm run build # Compiles TS to JS


##### RUN CONTAINER #####
