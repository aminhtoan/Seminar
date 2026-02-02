# 🎬 Telegram Movie Chatbot với n8n

Dự án xây dựng chatbot Telegram để tư vấn phim hay trong tuần và gợi ý rạp chiếu phim.

## 📋 Mục lục
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Tạo Telegram Bot](#tạo-telegram-bot)
- [Cấu hình n8n Workflow](#cấu-hình-n8n-workflow)
- [Các tính năng](#các-tính-năng)

## 🔧 Yêu cầu hệ thống
- Docker & Docker Compose
- Tài khoản Telegram
- (Tùy chọn) API key từ TMDB hoặc OMDb để lấy thông tin phim

## 🚀 Cài đặt

### 1. Khởi động Docker containers

```bash
# Di chuyển vào thư mục dự án
cd n8n-project

# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f
```

### 2. Truy cập n8n
- **URL**: http://localhost:5678
- **Username**: admin
- **Password**: admin123

## 🤖 Tạo Telegram Bot

### Bước 1: Tạo Bot với BotFather
1. Mở Telegram và tìm `@BotFather`
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (VD: "Movie Advisor Bot")
4. Đặt username cho bot (VD: "movie_advisor_bot")
5. **Lưu lại Bot Token** được cung cấp

### Bước 2: Cấu hình trong n8n
1. Truy cập n8n tại http://localhost:5678
2. Vào **Settings** > **Credentials** > **Add Credential**
3. Chọn **Telegram API**
4. Nhập Bot Token đã lưu

## 🔄 Cấu hình n8n Workflow

### Workflow 1: Movie Info Bot

Tạo workflow với các nodes sau:

```
[Telegram Trigger] → [Switch] → [HTTP Request (TMDB API)] → [Format Response] → [Telegram Send]
```

#### Các bước chi tiết:

1. **Telegram Trigger Node**
   - Trigger on: Message
   - Bot: Chọn credential đã tạo

2. **Switch Node** - Phân loại tin nhắn
   - Điều kiện 1: `/phimhay` → Lấy danh sách phim hot
   - Điều kiện 2: `/rapchieu` → Tìm rạp chiếu gần
   - Điều kiện 3: `/timphim` → Tìm kiếm phim

3. **HTTP Request Node** - Gọi API phim
   ```
   URL: https://api.themoviedb.org/3/movie/now_playing
   Method: GET
   Query Parameters:
     - api_key: YOUR_TMDB_API_KEY
     - language: vi-VN
     - region: VN
   ```

4. **Function Node** - Format kết quả
   ```javascript
   const movies = $input.first().json.results.slice(0, 5);
   
   let message = "🎬 *TOP PHIM HAY TUẦN NÀY*\n\n";
   
   movies.forEach((movie, index) => {
     message += `${index + 1}. *${movie.title}*\n`;
     message += `   ⭐ Điểm: ${movie.vote_average}/10\n`;
     message += `   📅 Khởi chiếu: ${movie.release_date}\n\n`;
   });
   
   return [{ json: { text: message } }];
   ```

5. **Telegram Send Node**
   - Chat ID: `{{ $('Telegram Trigger').item.json.message.chat.id }}`
   - Text: `{{ $json.text }}`
   - Parse Mode: Markdown

### Workflow 2: Cinema Finder

```
[Telegram Trigger] → [Extract Location] → [Google Places API] → [Format] → [Telegram Send]
```

## 🎯 Các tính năng

### Lệnh Bot hỗ trợ

| Lệnh | Mô tả |
|------|-------|
| `/start` | Bắt đầu và hướng dẫn sử dụng |
| `/phimhay` | Xem top phim hay trong tuần |
| `/rapchieu` | Tìm rạp chiếu phim gần đây |
| `/timphim [tên]` | Tìm kiếm thông tin phim |
| `/help` | Xem hướng dẫn sử dụng |

### Ví dụ tin nhắn trả về

```
🎬 TOP PHIM HAY TUẦN NÀY

1. Avengers: Endgame
   ⭐ Điểm: 8.5/10
   📅 Khởi chiếu: 2024-04-26

2. Oppenheimer
   ⭐ Điểm: 8.9/10
   📅 Khởi chiếu: 2024-04-20
...
```

## 🔑 API Keys cần thiết

### 1. TMDB API (Thông tin phim)
1. Đăng ký tại https://www.themoviedb.org/signup
2. Vào Settings > API > Request API Key
3. Lưu lại API Key

### 2. Google Places API (Tìm rạp chiếu - Tùy chọn)
1. Vào Google Cloud Console
2. Tạo project mới
3. Enable Places API
4. Tạo API Key

## 🛠️ Quản lý Docker

```bash
# Dừng tất cả services
docker-compose down

# Xem trạng thái
docker-compose ps

# Restart n8n
docker-compose restart n8n

# Xem logs của n8n
docker-compose logs -f n8n

# Xóa toàn bộ data (cẩn thận!)
docker-compose down -v
```

## 📁 Cấu trúc thư mục

```
n8n-project/
├── docker-compose.yml    # Cấu hình Docker services
├── README.md             # Hướng dẫn này
└── workflows/            # (Tùy chọn) Export workflows
    └── movie-bot.json
```

## 🔒 Bảo mật (Production)

Khi deploy production, hãy thay đổi:
1. `N8N_BASIC_AUTH_PASSWORD` - Mật khẩu mạnh hơn
2. `N8N_ENCRYPTION_KEY` - Key ngẫu nhiên
3. `POSTGRES_PASSWORD` - Mật khẩu database
4. Sử dụng HTTPS với reverse proxy (nginx/traefik)

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Tham khảo docs n8n: https://docs.n8n.io
