FROM node:20-alpine

WORKDIR /app

# Copy package files trước
COPY javascript/SimpleSocialMediaApplication/package*.json ./

# Cài đặt dependencies
RUN npm install

# Copy source code
COPY javascript/SimpleSocialMediaApplication/ .

# Expose port 3000
EXPOSE 3000

# Chạy dev server với host 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]