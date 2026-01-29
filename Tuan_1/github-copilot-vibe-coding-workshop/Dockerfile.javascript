# ===== Build stage =====
FROM node:20-alpine AS build
WORKDIR /app

# Copy package files trước để cache npm install
COPY javascript/SimpleSocialMediaApplication/package*.json ./
RUN npm install

# Copy source code
COPY javascript/SimpleSocialMediaApplication .
RUN npm run build

# ===== Runtime stage =====
FROM nginx:alpine

# Vite build output là /dist
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
