# Chọn image base (sử dụng JDK image)
FROM eclipse-temurin:21-jdk-jammy

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file jar vào container
COPY target/eureka-server-0.0.1-SNAPSHOT.jar /app/eureka-server.jar

# Chạy ứng dụng khi container bắt đầu
ENTRYPOINT ["java", "-jar", "/app/eureka-server.jar"]

# Cấu hình cổng mà ứng dụng sẽ lắng nghe
EXPOSE 8761