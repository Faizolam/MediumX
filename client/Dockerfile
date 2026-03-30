# ===== client/Dockerfile (Frontend - NOT NEEDED for GCP deployment) =====
# Note: This Dockerfile is not needed since we're serving frontend files 
# directly from Cloud Storage. But keeping it for local development.

FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend files to Nginx's default directory
COPY . /usr/share/nginx/html

# Remove the Dockerfile from the served files
RUN rm -f /usr/share/nginx/html/Dockerfile /usr/share/nginx/html/nginx.conf

# Expose the port
EXPOSE 80

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1










    
# #use an Nginx base image
# FROM nginx:alpine

# # Copy frontend files to Nginx's default directory
# COPY . /usr/share/nginx/html

# # Expose the port
# EXPOSE 80