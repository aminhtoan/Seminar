# ===== Stage 1: Build =====
FROM eclipse-temurin:21-jdk-jammy AS builder
WORKDIR /workspace

COPY java/socialapp/gradle ./gradle
COPY java/socialapp/gradlew .
COPY java/socialapp/gradlew.bat .
COPY java/socialapp/build.gradle .
COPY java/socialapp/settings.gradle .

RUN chmod +x ./gradlew
RUN ./gradlew dependencies --no-daemon

COPY java/socialapp/src ./src
RUN ./gradlew build --no-daemon -x test

# ===== Stage 2: Create custom JRE =====
FROM eclipse-temurin:21-jdk-jammy AS jre-builder

RUN jlink \
    --add-modules java.base,java.desktop,java.instrument,java.management,java.naming,java.net.http,java.security.jgss,java.sql,jdk.unsupported \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --compress=2 \
    --output /custom-jre

# ===== Stage 3: Runtime =====
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y ca-certificates sqlite3 curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=jre-builder /custom-jre /opt/java/openjdk

ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app
COPY --from=builder /workspace/build/libs/*.jar app.jar

RUN touch sns_api.db && \
    chown appuser:appuser sns_api.db && \
    chmod 664 sns_api.db && \
    chown -R appuser:appuser /app

USER appuser

ENV CODESPACE_NAME="${CODESPACE_NAME}"
ENV GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-jar", "app.jar"]
