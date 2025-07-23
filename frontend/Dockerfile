# ——— Build Stage ———
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

# The sole purpose of this stage is to build your React application. 
# It uses a Node.js environment to run npm install and npm run build. 
# This process takes your React code and compiles it down to a small 
# set of static files (HTML, CSS, and JavaScript) and places them in the /app/dist folder.
# Once this stage is complete, the entire Node.js environment (all the node_modules, source code, etc.) 
#is discarded. All we care about is the final output in /app/dist.

# ——— Serve Stage ———
# This stage creates the actual container that will run in production.
FROM nginx:alpine
# Copy build output
COPY --from=build /app/dist /usr/share/nginx/html

# No need to copy nginx.conf if you're not proxying here
# EXPOSE default port 80
EXPOSE 80

# Start nginx (default command)
# This is the most critical part for Docker. 
# By default, Nginx runs as a background "daemon." 
# If it did that, Docker would think the main process finished 
# and would immediately shut down the container. 
# This flag tells Nginx to run in the foreground, which keeps the container alive and serving your app.
CMD ["nginx", "-g", "daemon off;"]



