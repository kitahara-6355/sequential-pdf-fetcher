# スタディング PDF一括ダウンローダー (Studying Bulk PDF Downloader)

## 概要 (Overview)

このスクリプトは、オンライン学習サイト「スタディング」の講座ページからPDFテキストを一括でダウンロードするためのPythonスクリプトです。Playwrightを利用してブラウザを自動操作します。

This is a Python script to bulk download PDF textbooks from the online learning site "Studying". It uses Playwright to automate browser operations.

## 要件 (Requirements)

*   Python 3.9 以上 (Python 3.9 or higher)

## セットアップ手順 (Setup Instructions)

1.  **依存関係のインストール (Install Dependencies)**

    このディレクトリで、ターミナル（コマンドプロンプト）を開き、以下のコマンドを実行して必要なライブラリをインストールします。

    Open a terminal (command prompt) in this directory and run the following command to install the necessary libraries.

    ```bash
    pip install -r requirements.txt
    ```

2.  **ブラウザドライバのインストール (Install Browser Drivers)**

    次に、Playwrightがブラウザを操作するために必要なドライバをインストールします。

    Next, install the drivers that Playwright needs to control the browsers.

    ```bash
    playwright install
    ```
    *もしLinux環境で依存関係に関するエラーが出た場合は、`playwright install-deps` を実行してから再度お試しください。*
    *(If you encounter dependency errors in a Linux environment, please run `playwright install-deps` and then try again.)*


## 設定 (Configuration)

スクリプトを実行する前に、`main.py` ファイルを編集して、あなたの情報に合わせて設定を行う必要があります。

Before running the script, you need to edit the `main.py` file and configure it with your information.

1.  **ログイン情報とURLの設定 (Set Login Info and URL)**

    `main.py` をテキストエディタで開き、以下の項目を編集してください。

    Open `main.py` in a text editor and edit the following items:

    ```python
    # --- 設定 (User Configuration) ---
    USERNAME = "your_email@example.com"  # あなたのメールアドレスに書き換える
    PASSWORD = "your_password"           # あなたのパスワードに書き換える
    START_URL = "https://..."            # ダウンロードを開始したい最初の単元のURLに書き換える
    DOWNLOAD_COUNT = 300                 # ダウンロードしたい単元の総数
    # --- 設定ここまで (End of Configuration) ---
    ```

2.  **★重要★ セレクタの確認と変更 (★IMPORTANT★ Check and Change Selectors)**

    本スクリプトは、PDFダウンロードボタンと「次の単元へ」ボタンをクリックするために、CSSセレクタを使用しています。これらのセレクタはウェブサイトの構造変更によって変わる可能性があります。

    **もしスクリプトがボタンを見つけられずに止まってしまう場合は、ご自身で正しいセレクタを調べて設定し直す必要があります。**

    This script uses CSS selectors to click the PDF download button and the "Next Unit" button. These selectors may change due to website structure updates.

    **If the script stops because it cannot find the buttons, you will need to find the correct selectors yourself and update them.**

    **セレクタの調べ方 (How to find selectors):**
    a. ChromeやFirefoxブラウザでスタディングの単元ページを開きます。
    b. ボタンの上で右クリックし、「検証」または「要素を調査」を選択して開発者ツールを開きます。
    c. 開発者ツール上で、ボタンに対応するHTML要素（例: `<button class="c-button--pdf">` や `<a href="..." class="next-unit-link">`）がハイライトされます。
    d. その要素を一意に特定できるようなCSSセレクタ（例: `button.c-button--pdf`, `a.next-unit-link`）を考え、`main.py` の以下の部分を書き換えます。

    ```python
    # main.py の中のループ部分
    pdf_download_button_selector = "ここに正しいセレクタを記述"
    next_unit_button_selector = "ここに正しいセレクタを記述"
    ```

## 実行方法 (How to Run)

設定が完了したら、ターミナルで以下のコマンドを実行します。

Once the configuration is complete, run the following command in your terminal.

```bash
python studying_downloader/main.py
```

スクリプトが起動し、ブラウザが自動的に操作され、ダウンロードが開始されます。ダウンロードされたファイルは `downloads` フォルダに保存されます。

The script will start, the browser will be automated, and the download will begin. Downloaded files will be saved in the `downloads` folder.

## 免責事項 (Disclaimer)

*   このスクリプトは自己責任でご利用ください。
*   ウェブサイトの利用規約を遵守してください。
*   短時間に大量のリクエストを送信すると、ウェブサイトに過大な負荷をかける可能性があります。スクリプト内の待機時間 (`await page.wait_for_timeout(...)`) を適切に調整し、節度を持って使用してください。

*   Use this script at your own risk.
*   Please comply with the website's terms of service.
*   Sending a large number of requests in a short period can overload the website's servers. Please use this script responsibly by adjusting the wait times (`await page.wait_for_timeout(...)`) appropriately.
