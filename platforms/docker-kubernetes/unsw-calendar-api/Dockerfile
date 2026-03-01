####### BUILD IMAGE #######
FROM node:24-alpine AS build

# set working dir inside container 
WORKDIR /app       

# Enable pnpm via corepack
RUN corepack enable

# copy app files 
COPY package.json pnpm-lock.yaml ./

# install all dependencies 
RUN pnpm install --frozen-lockfile

# copy rest of source code
COPY . .

# compiles TS -> JS
RUN pnpm run build

##### RUN CONTAINER #####
FROM node:24-alpine AS production

WORKDIR /app

RUN corepack enable

# copy only prod dependencies
COPY package.json pnpm-lock.yaml ./

RUN pnpm install --prod --frozen-lockfile

# copy compiled code & prod dependencies 
COPY --from=build /app/dist ./dist

# setup app/non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# create cache directory and give ownership to user
RUN mkdir -p /app/cache && chown -R appuser:appgroup /app/cache
# switch to non-root user
USER appuser

# Listen on all interfaces
ENV HOST=0.0.0.0
ENV NODE_ENV=production
EXPOSE 3000

# start server
CMD ["node", "dist/server.js"]