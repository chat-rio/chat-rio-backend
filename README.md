# Hướng Dẫn Cài Đặt và Chạy Backend FastAPI

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant MongoDB
    participant Redis
    participant WebSocket
    participant Manager

    Client->>FastAPI: POST /register /login
    FastAPI-->>MongoDB: Tạo / Xác thực user
    FastAPI-->>Client: Trả JWT Token

    Client->>WebSocket: Connect ws://.../ws/{user_id}?token=...
    WebSocket->>FastAPI: websocket_endpoint()
    FastAPI->>FastAPI: verify_token()
    FastAPI->>Manager: connect(user_id, websocket)
    Manager-->>WebSocket: Accept()

    loop Receive WS event
        Client->>FastAPI: {event: "message", to, content}
        FastAPI->>MongoDB: Lưu message vào collection A_B
        FastAPI->>Redis: publish_message(payload)
        FastAPI->>Manager: Gửi lại cho người gửi

        Redis-->>FastAPI: redis_subscriber lắng nghe
        FastAPI->>Manager: Gửi message cho người nhận

        Client->>FastAPI: {event: "typing", to}
        FastAPI->>Redis: publish_message(typing)

        Client->>FastAPI: {event: "seen", to}
        FastAPI->>MongoDB: Update seen messages
        FastAPI->>Redis: publish_message(seen)
    end

    WebSocket-->>Manager: disconnect(user_id) (on error/close)

```

1. **Cài đặt môi trường ảo env**:

```bash
pip install virtualenv 
```

2. **tạo môi trường ảo với name myenv**:

```bash
python -m venv venv
```

3. **start môi trường ảo myenv**:

```bash
venv\Scripts\activate
```

4. **Cài đặt các phụ thuộc**:

```bash
pip install -r requirements.txt
```

5. **Chạy ứng dụng**:

```bash
python run.py
```

6. **Biến môi trường**:

| Tên biến môi trường      | Giá trị               | Mô tả                               |
| ------------------------ | --------------------- | ----------------------------------- |
| SECRET_KEY        | your_super_secret_key | secret key |
| MONGO_URI    | mongodb://localhost:27017/ | Url mongodb                     |
| MONGO_DB | __________| mongodb name | 
|ALGORITHM | __________ | Thuật toán đối xứng jwt|
|REDIS_URL| redis://localhost:6379| redis |
