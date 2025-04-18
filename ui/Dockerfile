# ---------- Stage 1: Build Vite app ----------
FROM node:20 AS builder

WORKDIR /app

RUN npm install -g pnpm
COPY package.json pnpm-lock.yaml ./
RUN pnpm install
COPY . .
RUN pnpm run build

# ---------- Stage 2: Serve with Nginx ----------
FROM nginx:alpine AS prod

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built files from previous stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# ---------- Stage 3: Dev image ----------
FROM node:20 AS dev

WORKDIR /app
RUN npm install -g pnpm

# Optional: preload deps for faster boot
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .

CMD ["pnpm", "dev", "--host"]
