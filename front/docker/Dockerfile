FROM node:20-alpine AS development-dependencies-env
COPY app/ /app
WORKDIR /app
RUN npm install

FROM node:20-alpine AS production-dependencies-env
COPY app/package.json /app/
WORKDIR /app
RUN npm install --omit=dev

FROM node:20-alpine AS build-env
COPY app/ /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm run build

FROM node:20-alpine
COPY app/ /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
COPY docker/scripts/health_check.sh /app/docker/scripts/health_check.sh
RUN chmod +x /app/docker/scripts/health_check.sh
WORKDIR /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]