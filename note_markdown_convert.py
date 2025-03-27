import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def HtmlToMarkdownAndImagesFromUrl(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_content = md(html_content)

    # 画像の URL を取得し、絶対 URL に変換
    image_urls = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        full_url = urljoin(url, src)
        image_urls.append(full_url)
    return html_content, markdown_content, image_urls

def FilterContent(markdown_content):
    new_content = []
    code_block = False
    article_started = False
    article_ended = False

    # コードブロック内でのタグの無視と記事の始まり・終わりの抽出
    for line in markdown_content.splitlines():
        # コードブロックの開始または終了を検出
        if line.strip().startswith("```"):
            code_block = not code_block
        
        # コードブロック外の処理
        if not code_block:
            if "[--記事始まり--]" in line and not article_started:
                article_started = True
                continue  # 記事の始まりタグは含めない
            elif "[--記事終わり--]" in line and article_started:
                article_ended = True
                break  # 記事の終わりで抽出を終了

        # 記事が始まってから終わるまでの内容を追加
        if article_started and not article_ended:
            new_content.append(line)

    # 抽出した内容がない場合はNoneを返す
    return '\n'.join(new_content) if new_content else None




"""
def SaveMarkdownAndImages(html_content, markdown_content, image_urls, base_dir, markdown_filename, url):
    markdown_content = FilterContent(markdown_content)  # 抽出した内容のみを保存する

    # フォルダの設定
    folder_name = urlparse(url).netloc.replace('.', '_')
    output_dir = os.path.join(base_dir, folder_name)
    content_dir = os.path.join(output_dir, 'Content')
    images_dir = os.path.join(output_dir, 'Images')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # HTML と Markdown ファイルを保存
    html_path = os.path.join(content_dir, 'original.html')
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"HTML saved: {html_path}")

    markdown_path = os.path.join(content_dir, markdown_filename)
    with open(markdown_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Markdown saved: {markdown_path}")

    # 画像を保存してマッピングを作成
    image_mappings = {}
    for index, image_url in enumerate(image_urls, 1):
        image_name = f"{index:03d}.png"
        image_path = os.path.join(images_dir, image_name)
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            image_mappings[image_url] = image_name
            print(f"Image saved: {image_path}")
        except requests.RequestException as e:
            print(f"Failed to retrieve image from {image_url}: {e}")

    # Markdownファイルの画像リンクを更新
    for original_url, new_filename in image_mappings.items():
        markdown_content = markdown_content.replace(original_url, new_filename)

    # 更新されたマークダウン内容をファイルに再保存
    with open(markdown_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Updated Markdown saved: {markdown_path}")

    return content_dir, image_mappings

"""
def SaveMarkdownAndImages(html_content, markdown_content, image_urls, base_dir, markdown_filename, url):
    filtered_markdown = FilterContent(markdown_content)  # 抽出した内容のみを保存する
    if filtered_markdown is None:
        filtered_markdown = markdown_content  # フィルタリング後が空なら元のMarkdownを使う

    # フォルダの設定
    folder_name = urlparse(url).netloc.replace('.', '_')
    output_dir = os.path.join(base_dir, folder_name)
    content_dir = os.path.join(output_dir, 'Content')
    images_dir = os.path.join(output_dir, 'Images')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # HTML と Markdown ファイルを保存
    html_path = os.path.join(content_dir, 'original.html')
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"HTML saved: {html_path}")

    markdown_path = os.path.join(content_dir, markdown_filename)
    with open(markdown_path, 'w', encoding='utf-8') as file:
        file.write(filtered_markdown)  # None でないことを保証
    print(f"Markdown saved: {markdown_path}")

    # 画像を保存してマッピングを作成
    image_mappings = {}
    for index, image_url in enumerate(image_urls, 1):
        image_name = f"{index:03d}.png"
        image_path = os.path.join(images_dir, image_name)
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            image_mappings[image_url] = image_name
            print(f"Image saved: {image_path}")
        except requests.RequestException as e:
            print(f"Failed to retrieve image from {image_url}: {e}")

    # Markdownファイルの画像リンクを更新
    for original_url, new_filename in image_mappings.items():
        filtered_markdown = filtered_markdown.replace(original_url, new_filename)

    # 更新されたマークダウン内容をファイルに再保存
    with open(markdown_path, 'w', encoding='utf-8') as file:
        file.write(filtered_markdown)
    print(f"Updated Markdown saved: {markdown_path}")

    return content_dir, image_mappings


# 使用例
url = 'https://note.com/madoka235/n/n1ef15bbabcad'
base_dir = os.getcwd()
html_content, markdown_content, image_urls = HtmlToMarkdownAndImagesFromUrl(url)
markdown_filename = 'example.md'
content_dir, image_mappings = SaveMarkdownAndImages(html_content, markdown_content, image_urls, base_dir, markdown_filename, url)


def read_markdown(file_path):
    """指定されたファイルから内容を読み込み、その文字列を返す"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_qiita_markdown(markdown_content, image_mappings, content_dir, qiita_markdown_filename):
    """Markdownの内容をQiita用に修正し、指定されたディレクトリに保存する"""
    lines = markdown_content.split('\n')
    qiita_content = []
    image_index = 1  # 画像のインデックスを初期化
    in_link = False  # リンクブロック内かどうかのフラグ
    collected_link = ''  # 複数行にまたがるリンクの収集

    for line in lines:
        # urlの変換
        if line.startswith('[') or in_link:
            in_link = True
            collected_link += line
            if ')' in line:
                start = collected_link.find('http')
                end = collected_link.find(')', start)
                if start != -1 and end != -1:
                    qiita_content.append(collected_link[start:end])
                in_link = False
                collected_link = ''
            continue
        # 見出し変換の制御
        if line.startswith('------------------------'):
            last_line = qiita_content.pop()  # 最後の行を取得
            qiita_content.append(f"## {last_line}")  # 見出しとして再フォーマット
            continue
                # 見出し変換の制御
        if line.startswith('------'):
            last_line = qiita_content.pop()  # 最後の行を取得
            qiita_content.append(f"## {last_line}")  # 見出しとして再フォーマット
            continue
        if line.startswith('---'):
            last_line = qiita_content.pop()  # 最後の行を取得
            qiita_content.append(f"## {last_line}")  # 見出しとして再フォーマット
            continue
        

        # 画像のURLをQiita用の形式に変換
        if '![](' in line:
            for original_url, new_filename in image_mappings.items():
                if original_url in line:
                    line = line.replace(original_url, f"../Images/{new_filename}")
                    break  # 一致するものが見つかったらループを抜ける

        # 箇条書きの形式を修正
        if line.strip().startswith('* ') or line.strip().startswith('+ '):
            line = line.replace('* ', '- ').replace('+ ', '- ')

        qiita_content.append(line)

    qiita_markdown = '\n'.join(qiita_content)
    
    qiita_markdown_path = os.path.join(content_dir, qiita_markdown_filename)
    with open(qiita_markdown_path, 'w', encoding='utf-8') as file:
        file.write(qiita_markdown)
    print(f"Qiita Markdown saved: {qiita_markdown_path}")

# 使用例
base_dir = os.getcwd()
content_dir = os.path.join(base_dir, 'note_com', 'Content')
example_md_path = os.path.join(content_dir, 'example.md')
markdown_content = read_markdown(example_md_path)

# 画像のマッピング情報をここで定義するか、別の方法で取得する
# 例: image_mappings = {'https://example.com/image1.png': '001.png', 'https://example.com/image2.png': '002.png'}
image_mappings = {
    # ...他の画像も同様に...
}

qiita_markdown_filename = 'fixQiita.md'
save_qiita_markdown(markdown_content, image_mappings, content_dir, qiita_markdown_filename)


