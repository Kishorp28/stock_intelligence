# ==========================================
# STAGE 1: Build the React Application natively
# ==========================================
FROM node:20-alpine AS build

WORKDIR /app

# First install dependencies for caching advantages
COPY package*.json ./
RUN npm install

# Build the optimized production SPA
COPY . .
RUN npm run build

# ==========================================
# STAGE 2: Serve natively using Nginx Proxy
# ==========================================
FROM nginx:stable-alpine

# Remove default nginx structural payload
RUN rm -rf /usr/share/nginx/html/*

# Copy Vite build configurations (dist folder) directly to the web-server
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP standard port
EXPOSE 80

# Start server natively
CMD ["nginx", "-g", "daemon off;"]
