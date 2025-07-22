FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install deps
COPY frontend/package*.json ./
RUN npm install

# Copy env (so VITE_API_URL is inlined) and source
COPY frontend/.env.local ./
COPY frontend/ .

# Build production assets
RUN npm run build

# ——— Serve stage ———
FROM nginx:alpine
# Copy build output
COPY --from=build /app/dist /usr/share/nginx/html

# No need to copy nginx.conf if you're not proxying here
# EXPOSE default port 80
EXPOSE 80

# Start nginx (default command)
CMD ["nginx", "-g", "daemon off;"]


