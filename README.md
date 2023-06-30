# HƯỚNG DẪN SỬ DỤNG
Tài liệu chương trình và video demo:
https://drive.google.com/drive/folders/162j9JjoV6o6ES7tCpXeflUOetSmeaoPF?usp=sharing

## Ứng dụng Flask
### Cài đặt
#### Unix / MacOS

1. Cài đặt các module cần thiết bằng cách sử dụng `venv`:

   ```bash
   $ virtualenv env
   $ source env/bin/activate
   $ pip3 install -r requirements.txt
   ```

### Cấu hình Flask
1. Thiết lập các biến môi trường cho Flask:

   ```bash
   $ export FLASK_APP=run.py
   $ export FLASK_ENV=development
   ```

Đặt các biến sau theo thông tin kết nối đến MySQL
```bash
export DB_ENGINE=mysql+mysqlconnector
export DB_USERNAME=root  
export DB_PASS=<...>
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=IntroAI   
```

## Khởi chạy ứng dụng

Khởi chạy ứng dụng:

```bash
$ flask run
```

Hoặc, để chạy ứng dụng với giao thức HTTPS, sử dụng lệnh sau:

```bash
$ flask run --cert=adhoc
```

Ứng dụng sẽ được truy cập qua địa chỉ http://127.0.0.1:5000/.