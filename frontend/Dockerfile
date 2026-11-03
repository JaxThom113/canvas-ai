# Builds the Chrome extension and copies it (plus a zip) to /out on start
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build


FROM alpine:3.22

RUN apk add --no-cache zip
COPY --from=build /app/dist /dist

CMD ["sh", "-c", "rm -rf /out/canvy && cp -r /dist /out/canvy && cd /dist && rm -f /out/canvy.zip && zip -qr /out/canvy.zip . && echo 'Extension built to build/canvy (zip: build/canvy.zip)'"]
