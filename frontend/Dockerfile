FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application
COPY . .

# Build for production
RUN npm run build

# Expose port
EXPOSE 5173

# Serve with vite preview or use a static server
CMD ["npm", "run", "preview"]
