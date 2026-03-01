####### BUILD IMAGE #######
FROM node:20-alpine AS build

# set working dir inside container 
WORKDIR /app        

# copy app files 
COPY package*.json ./

# install all dependencies 
RUN npm ci

# copy rest of source code
COPY . .

# compiles TS -> JS
RUN npm run build

##### RUN CONTAINER #####
FROM node:20-alpine AS production

WORKDIR /app

# copy compiled code & prod dependencies 
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json

# install only prod dependencies
RUN npm ci --production

# setup app/non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

ENV NODE_ENV=production

EXPOSE 3000

# start server
CMD ["node", "dist/server.js"]