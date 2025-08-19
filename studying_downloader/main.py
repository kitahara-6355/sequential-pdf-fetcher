import asyncio
from playwright.async_api import async_playwright

# --- 設定 (User Configuration) ---
# ユーザー名とパスワードをここに設定してください
# Please set your username and password here
USERNAME = "your_email@example.com"
PASSWORD = "your_password"

# スタディングのログインページのURL
# URL for the Studing login page
LOGIN_URL = "https://www.studying.jp/login"

# 最初の単元のページのURL
# URL of the first unit's page to start downloading from
START_URL = "https://www.studying.jp/course/path/to/first/unit"

# ダウンロードする単元の数
# Number of units to download
DOWNLOAD_COUNT = 300

# ダウンロード先のディレクトリ
# Directory to save downloaded files
DOWNLOAD_DIR = "downloads"
# --- 設定ここまで (End of Configuration) ---

async def main():
    """
    メインの自動化処理
    Main automation process
    """
    async with async_playwright() as p:
        # headless=Falseにするとブラウザの動きが実際に見えるため、デバッグに便利です
        # Setting headless=False allows you to see the browser, which is useful for debugging
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # 1. ログイン処理 (Login Process)
        print(f"ログインページにアクセスします: {LOGIN_URL}")
        await page.goto(LOGIN_URL)

        # ユーザー名とパスワードを入力
        # Fill in username and password
        print("ログイン情報を入力しています...")
        # 実際のサイトの要素に合わせてセレクタを調整してください
        # Please adjust the selectors to match the actual elements on the site
        await page.get_by_placeholder("メールアドレス").fill(USERNAME)
        await page.get_by_placeholder("パスワード").fill(PASSWORD)

        # ログインボタンをクリック
        # Click the login button
        await page.get_by_role("button", name="ログイン").click()

        print("ログイン処理を実行しました。マイページへの遷移を待ちます...")
        # ログイン後、マイページやコース一覧ページに遷移するのを待ちます
        # After login, wait for navigation to the "my page" or course list page
        await page.wait_for_url("**/mycourses**", timeout=60000)
        print("ログイン成功。")

        # 2. 最初の単元ページに移動 (Navigate to the first unit page)
        print(f"最初の単元ページに移動します: {START_URL}")
        await page.goto(START_URL)

        # 3. ダウンロードループ (Download Loop)
        for i in range(DOWNLOAD_COUNT):
            print(f"--- 単元 {i + 1}/{DOWNLOAD_COUNT} ---")

            # ▼▼▼ PDFダウンロード処理 (PDF Download Process) ▼▼▼
            # 注意: 実際のダウンロードボタンのセレクタに合わせて変更してください
            # Note: Please change the selector to match the actual download button
            pdf_download_button_selector = "button.c-button--pdf" # これはCSSセレクタの例です (This is an example CSS selector)

            try:
                print("PDFダウンロードボタンを待っています...")
                # ダウンロードイベントを待機する準備
                async with page.expect_download() as download_info:
                    # ダウンロードボタンをクリック
                    await page.locator(pdf_download_button_selector).click()

                download = await download_info.value
                save_path = f"{DOWNLOAD_DIR}/{download.suggested_filename}"
                await download.save_as(save_path)
                print(f"PDFを保存しました: {save_path}")

            except Exception as e:
                print(f"PDFのダウンロードに失敗しました: {e}")
                print("この単元をスキップします。")
                # 必要に応じてエラー時の待機時間を設ける
                await page.wait_for_timeout(5000) # 5秒待機

            # ▼▼▼ 「次の単元」への遷移 (Navigate to the "Next Unit") ▼▼▼
            # 注意: 実際の「次の単元」ボタンのセレクタに合わせて変更してください
            # Note: Please change the selector to match the actual "Next Unit" button
            next_unit_button_selector = "a.next-unit-link" # これはCSSセレクタの例です (This is an example CSS selector)

            try:
                print("「次の単元へ」ボタンをクリックします。")
                await page.locator(next_unit_button_selector).click()
                # ページの読み込みを待つ
                await page.wait_for_load_state("domcontentloaded")
                print("次の単元に移動しました。")
            except Exception as e:
                print(f"次の単元への移動に失敗しました: {e}")
                print("処理を中断します。")
                break

            # サーバーへの負荷を軽減するための待機時間
            await page.wait_for_timeout(3000) # 3秒待機

        print("--- 全ての処理が完了しました ---")
        await browser.close()

if __name__ == "__main__":
    # 設定の検証 (Validate configuration)
    if USERNAME == "your_email@example.com" or PASSWORD == "your_password":
        print("エラー: スクリプトを実行する前に、USERNAMEとPASSWORDを設定してください。")
        print("Error: Please set USERNAME and PASSWORD before running the script.")
    elif START_URL == "https://www.studying.jp/course/path/to/first/unit":
        print("エラー: スクリプトを実行する前に、START_URLを正しい講座のURLに設定してください。")
        print("Error: Please set the START_URL to the correct course URL before running the script.")
    else:
        # ダウンロード用ディレクトリを作成 (Create download directory)
        import os
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        asyncio.run(main())
