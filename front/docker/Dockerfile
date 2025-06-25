FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY app/package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY app/ ./

# Copy health check script (from docker/scripts relative to build context)
COPY docker/scripts/health_check.sh /app/docker/scripts/health_check.sh
RUN chmod +x /app/docker/scripts/health_check.sh

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]