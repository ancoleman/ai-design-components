# Java Dockerfiles

Complete patterns for containerizing Java applications with Maven and Gradle.

## Table of Contents

1. [Base Image Selection](#base-image-selection)
2. [Pattern 1: Maven Multi-Stage](#pattern-1-maven-multi-stage)
3. [Pattern 2: Gradle Multi-Stage](#pattern-2-gradle-multi-stage)
4. [Pattern 3: Spring Boot](#pattern-3-spring-boot)
5. [JVM Optimization](#jvm-optimization)
6. [Common Java Pitfalls](#common-java-pitfalls)

## Base Image Selection

**Recommended Java base images:**

| Build Stage | Runtime Stage | Final Size | Use Case |
|-------------|---------------|------------|----------|
| `maven:3.9-eclipse-temurin-21` | `eclipse-temurin:21-jre-alpine` | 200-350MB | Production (recommended) |
| `gradle:8-jdk21` | `eclipse-temurin:21-jre-alpine` | 200-350MB | Gradle projects |
| `maven:3.9-eclipse-temurin-17` | `eclipse-temurin:17-jre-alpine` | 180-320MB | Java 17 projects |
| `maven:3.9-eclipse-temurin-21` | `gcr.io/distroless/java21-debian12` | 250-400MB | Maximum security |

**Version pinning:**
```dockerfile
# ✅ Good: Exact version
FROM eclipse-temurin:21.0.1-jre-alpine

# ⚠️ OK: Minor version pinned
FROM eclipse-temurin:21-jre-alpine

# ❌ Bad: Unpredictable
FROM eclipse-temurin:jre-alpine
FROM openjdk:latest
```

## Pattern 1: Maven Multi-Stage

**Use when:**
- Standard Maven projects
- Spring Boot applications
- Traditional Java applications

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .

# Download dependencies (cached layer)
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

# Copy source code
COPY src ./src

# Build application
RUN --mount=type=cache,target=/root/.m2 \
    mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy JAR from builder
COPY --from=builder /app/target/*.jar app.jar

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# JVM options
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**Key features:**
- Dependency caching with BuildKit
- JRE-only runtime (no JDK)
- Non-root user
- Container-aware JVM settings
- Health check for Spring Boot actuator

**Build command:**
```bash
docker build -t java-app:latest .
```

**Expected size:** 250-350MB

## Pattern 2: Gradle Multi-Stage

**Use when:**
- Gradle-based projects
- Android backend services
- Kotlin applications

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM gradle:8-jdk21 AS builder

WORKDIR /app

# Copy Gradle files for dependency caching
COPY build.gradle settings.gradle ./
COPY gradle ./gradle

# Download dependencies (cached layer)
RUN --mount=type=cache,target=/root/.gradle \
    gradle dependencies --no-daemon

# Copy source code
COPY src ./src

# Build application
RUN --mount=type=cache,target=/root/.gradle \
    gradle clean build -x test --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy JAR from builder
COPY --from=builder /app/build/libs/*.jar app.jar

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# JVM options
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**Key Gradle commands:**
- `gradle dependencies` → Download dependencies only
- `gradle build -x test` → Build without running tests
- `--no-daemon` → Don't start Gradle daemon (Docker doesn't need it)

**Build command:**
```bash
docker build -t gradle-app:latest .
```

**Expected size:** 250-350MB

## Pattern 3: Spring Boot

**Optimized Spring Boot Dockerfile with layered JARs:**

```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml
COPY pom.xml .

# Download dependencies
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

# Copy source
COPY src ./src

# Build with layers enabled
RUN --mount=type=cache,target=/root/.m2 \
    mvn clean package -DskipTests && \
    java -Djarmode=layertools -jar target/*.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy layers separately for better caching
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# JVM options
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"

# Spring Boot actuator health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.JarLauncher"]
```

**pom.xml configuration:**
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <layers>
                    <enabled>true</enabled>
                </layers>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**Layered JAR benefits:**
- Better layer caching (dependencies change less than application code)
- Faster rebuilds when only application code changes
- Smaller layer pushes to registry

**Expected size:** 280-380MB

## JVM Optimization

### Container-Aware JVM Settings

**Modern JVMs (Java 10+) are container-aware:**

```dockerfile
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
```

**Key flags:**
- `-XX:+UseContainerSupport` → Respect container memory limits
- `-XX:MaxRAMPercentage=75.0` → Use 75% of container memory for heap
- `-XX:InitialRAMPercentage=50.0` → Initial heap size
- `-XX:MinRAMPercentage=50.0` → Minimum heap size for small containers

### Garbage Collector Selection

**G1GC (default, recommended):**
```dockerfile
ENV JAVA_OPTS="-XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

**ZGC (low latency):**
```dockerfile
ENV JAVA_OPTS="-XX:+UseZGC -XX:+ZGenerational"
```

**Shenandoah (low latency alternative):**
```dockerfile
ENV JAVA_OPTS="-XX:+UseShenandoahGC"
```

### Memory Configuration

**For 512MB container:**
```dockerfile
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 -XX:InitialRAMPercentage=50.0"
# Heap: ~384MB max, ~256MB initial
```

**For 2GB container:**
```dockerfile
ENV JAVA_OPTS="-XX:MaxRAMPercentage=70.0"
# Heap: ~1.4GB
```

### Diagnostic Options

**Enable JVM diagnostics:**
```dockerfile
ENV JAVA_OPTS="-XX:+PrintCommandLineFlags -XX:+PrintGCDetails -XX:+PrintGCTimeStamps"
```

**Heap dump on OutOfMemoryError:**
```dockerfile
ENV JAVA_OPTS="-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/app/heapdumps"
```

## Common Java Pitfalls

### Pitfall 1: Using JDK in Runtime

**Problem:** JDK is much larger than JRE.

```dockerfile
# ❌ JDK in runtime (500MB+)
FROM eclipse-temurin:21
COPY app.jar .
CMD ["java", "-jar", "app.jar"]
```

**Solution:** Use JRE in runtime stage:
```dockerfile
# ✅ JRE only (200MB)
FROM eclipse-temurin:21-jre-alpine
COPY app.jar .
CMD ["java", "-jar", "app.jar"]
```

### Pitfall 2: Not Caching Dependencies

**Problem:** Re-downloads dependencies every build.

```dockerfile
# ❌ Re-downloads every time
COPY . .
RUN mvn package
```

**Solution:** Copy pom.xml first, cache dependencies:
```dockerfile
# ✅ Cached dependencies
COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    mvn package
```

### Pitfall 3: Not Setting Memory Limits

**Problem:** JVM doesn't respect container limits (older Java).

```dockerfile
# ❌ JVM may use more than container limit
CMD ["java", "-jar", "app.jar"]
```

**Solution:** Use container-aware settings:
```dockerfile
# ✅ Container-aware JVM
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### Pitfall 4: Running Tests in Docker Build

**Problem:** Slow builds, external dependencies may fail.

```dockerfile
# ❌ Runs tests during build (slow, flaky)
RUN mvn clean package
```

**Solution:** Skip tests, run in CI separately:
```dockerfile
# ✅ Skip tests in Docker build
RUN mvn clean package -DskipTests
```

### Pitfall 5: Not Using Layered JARs (Spring Boot)

**Problem:** Application code changes invalidate entire JAR layer.

```dockerfile
# ❌ Entire JAR in one layer
COPY --from=builder /app/target/*.jar app.jar
# Small code change = entire 100MB JAR re-pushed
```

**Solution:** Use layered JARs:
```dockerfile
# ✅ Separate layers (dependencies cached)
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/application/ ./
# Small code change = only application layer re-pushed (~10MB)
```

## Distroless Java Example

**Maximum security with distroless:**

```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    mvn clean package -DskipTests

# Runtime stage: distroless Java
FROM gcr.io/distroless/java21-debian12

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

USER nonroot:nonroot

# Note: JAVA_OPTS via environment, not command line
ENV JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Key differences with distroless:**
- No shell → Use `ENTRYPOINT ["java", ...]` directly
- No sh → Can't use `sh -c`
- Set JVM options via `JAVA_TOOL_OPTIONS` environment variable
- Built-in nonroot user (UID 65532)

**Expected size:** 300-450MB

## Complete Spring Boot Example

**Production-ready Spring Boot microservice:**

```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy Maven files
COPY pom.xml .
COPY .mvn .mvn

# Download dependencies
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

# Copy source
COPY src ./src

# Build with layers
RUN --mount=type=cache,target=/root/.m2 \
    mvn clean package -DskipTests && \
    java -Djarmode=layertools -jar target/*.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy layers
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

# JVM options
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:+UseG1GC \
    -Dspring.profiles.active=prod"

# Health check (Spring Boot Actuator)
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health/liveness || exit 1

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.JarLauncher"]
```

**application.yml:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      probes:
        enabled: true
```

**Expected size:** 300-400MB

## Summary

**Java Dockerfile patterns ranked:**

| Pattern | Size | Build Speed | Use Case |
|---------|------|-------------|----------|
| Maven + JRE Alpine | 250-350MB | Medium | Production (recommended) |
| Gradle + JRE Alpine | 250-350MB | Medium | Gradle projects |
| Spring Boot Layered | 280-380MB | Fast | Spring Boot apps |
| Distroless Java | 300-450MB | Medium | Maximum security |

**Key takeaways:**
- Always use multi-stage builds (JDK for build, JRE for runtime)
- Use BuildKit cache mounts for Maven/Gradle dependencies
- Enable Spring Boot layered JARs for better caching
- Use container-aware JVM settings (`-XX:+UseContainerSupport`)
- Set MaxRAMPercentage to 70-75% of container memory
- Use JRE Alpine images for smallest size
- Create non-root user
- Skip tests in Docker build (run in CI)
- Pin Java version
- Use actuator health checks for Spring Boot
