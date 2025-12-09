import requests
import json
import time
import os
from googletrans import Translator


def fetch_btc_price():
    """Lấy và hiển thị giá Bitcoin từ API CoinPaprika."""
    print("--- Đang lấy giá Bitcoin ---")
    try:
        # Lấy dữ liệu giá Bitcoin từ API CoinPaprika
        response = requests.get("https://api.coinpaprika.com/v1/tickers/btc-bitcoin")
        response.raise_for_status()  # Báo lỗi nếu yêu cầu không thành công (status code 4xx hoặc 5xx)

        data = response.json()
        usd_quote = data.get('quotes', {}).get('USD', {})

        if usd_quote and 'price' in usd_quote:
            # Trích xuất giá Bitcoin bằng USD
            btc_price = usd_quote['price']
            print(f"Giá Bitcoin (USD): ${btc_price:,.2f}")

            # Tùy chọn: In các thông tin hữu ích khác
            print(f"Khối lượng 24h: ${usd_quote.get('volume_24h', 0):,.2f}")
            print(f"Vốn hóa thị trường: ${usd_quote.get('market_cap', 0):,.2f}")
            print(f"Thay đổi 24h: {usd_quote.get('percent_change_24h', 0)}%")
        else:
            print("Lỗi: Không tìm thấy dữ liệu giá USD trong phản hồi.")

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi thực hiện yêu cầu lấy giá: {e}")
    except json.JSONDecodeError:
        print("Lỗi: Không thể giải mã JSON từ phản hồi giá.")

def fetch_crypto_news(translator):
    """Lấy và hiển thị tin tức tiền điện tử từ API CryptoCompare."""
    print("\n--- Đang lấy tin tức mới nhất ---")
    try:
        # Lấy tin tức từ API CryptoCompare (lấy 5 tin mới nhất)
        response = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN&limit=5")
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("Type") == 100 and "Data" in data:
            print("Đã tìm thấy tin tức, đang dịch sang tiếng Việt...")
            for index, article in enumerate(data["Data"], 1):
                title_en = article.get('title', 'Không có tiêu đề')
                body_en = article.get('body', 'Không có tóm tắt')

                try:
                    # Dịch tiêu đề và tóm tắt sang tiếng Việt
                    title_vi = translator.translate(title_en, dest='vi').text
                    body_vi = translator.translate(body_en, dest='vi').text
                except Exception as e:
                    print(f"Lỗi dịch: {e}. Hiển thị bản gốc.")
                    title_vi = title_en
                    body_vi = body_en

                print("-" * 20)
                print(f"TIN TỨC #{index}")
                print(f"Tiêu đề: {title_vi}")
                print(f"Nguồn: {article.get('source', 'Không có nguồn')}")
                print(f"Tóm tắt: {body_vi}...")
                print(f"Đọc thêm: {article.get('url', 'Không có link')}")
        else:
            print("Lỗi: Không tìm thấy dữ liệu tin tức trong phản hồi.")
            
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi thực hiện yêu cầu lấy tin tức: {e}")
    except json.JSONDecodeError:
        print("Lỗi: Không thể giải mã JSON từ phản hồi tin tức.")

def clear_screen():
    """Xóa màn hình console."""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    UPDATE_INTERVAL_SECONDS = 600  # Cập nhật mỗi 10 phút (10 * 60 = 600 giây)
    translator = Translator()

    try:
        while True:
            clear_screen()
            print(f"Cập nhật lần cuối lúc: {time.strftime('%H:%M:%S')}")
            fetch_btc_price()
            fetch_crypto_news(translator)
            print(f"\nSẽ tự động cập nhật lại sau {UPDATE_INTERVAL_SECONDS // 60} phút...")
            time.sleep(UPDATE_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")    