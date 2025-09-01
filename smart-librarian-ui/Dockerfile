# DOCKER FILE LOCAL CU DOCKER COMPOSE UP
FROM node:20-alpine

WORKDIR /smart-librarian-ui

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# DOCKER FILE PT. Azure
# FROM node:18-alpine AS build
# WORKDIR /smart-librarian-ui
# COPY . .
# COPY .env .env
# RUN npm install && npm run build

# FROM nginx:alpine
# COPY --from=build /smart-librarian-ui/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]