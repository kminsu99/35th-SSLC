import os
import re
import html
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client


# ============================================================
# 1. 환경변수
# ============================================================

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_NOTION_TO_HTML_PAGE_ID")

if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN이 .env에 없습니다.")

if not NOTION_PARENT_PAGE_ID:
    raise ValueError("NOTION_PARENT_PAGE_ID가 .env에 없습니다.")


notion = Client(auth=NOTION_TOKEN)


# ============================================================
# 2. 파일명으로 사용할 수 있도록 페이지 제목 정리
# ============================================================

def make_filename(title):
    """
    Notion 페이지 제목을 HTML 파일명으로 변환
    """

    # Windows에서 파일명에 사용할 수 없는 문자 제거
    title = re.sub(r'[<>:"/\\|?*]', '_', title)

    # 앞뒤 공백 제거
    title = title.strip()

    # 빈 제목인 경우
    if not title:
        title = "untitled"

    return f"{title}.html"


# ============================================================
# 3. Rich Text → HTML
# ============================================================

def rich_text_to_html(rich_text):
    result = []

    for item in rich_text:

        text = html.escape(
            item.get("plain_text", "")
        )

        annotations = item.get("annotations", {})

        if annotations.get("bold"):
            text = f"<strong>{text}</strong>"

        if annotations.get("italic"):
            text = f"<em>{text}</em>"

        if annotations.get("strikethrough"):
            text = f"<del>{text}</del>"

        if annotations.get("underline"):
            text = f"<u>{text}</u>"

        if annotations.get("code"):
            text = f"<code>{text}</code>"

        # 링크
        href = item.get("href")

        if href:
            href = html.escape(href, quote=True)

            text = (
                f'<a href="{href}" '
                f'target="_blank" '
                f'rel="noopener noreferrer">'
                f'{text}</a>'
            )

        result.append(text)

    return "".join(result)


# ============================================================
# 4. 블록 가져오기
# ============================================================

def get_blocks(block_id):

    blocks = []
    cursor = None

    while True:

        params = {
            "block_id": block_id,
            "page_size": 100
        }

        if cursor:
            params["start_cursor"] = cursor

        response = notion.blocks.children.list(**params)

        blocks.extend(response["results"])

        if not response["has_more"]:
            break

        cursor = response["next_cursor"]

    return blocks


# ============================================================
# 5. 페이지 제목 가져오기
# ============================================================

def get_page_title(page):

    properties = page.get("properties", {})

    for prop in properties.values():

        if prop.get("type") == "title":

            title_list = prop.get("title", [])

            if title_list:
                return "".join(
                    item.get("plain_text", "")
                    for item in title_list
                )

    return "untitled"


# ============================================================
# 6. 블록 → HTML
# ============================================================

def blocks_to_html(blocks):

    output = []

    for block in blocks:

        block_type = block["type"]
        data = block[block_type]

        rich_text = data.get("rich_text", [])

        content = rich_text_to_html(rich_text)

        # ----------------------------------------------------
        # paragraph
        # ----------------------------------------------------

        if block_type == "paragraph":

            if content:
                output.append(
                    f"<p>{content}</p>"
                )

        # ----------------------------------------------------
        # heading
        # ----------------------------------------------------

        elif block_type == "heading_1":

            output.append(
                f"<h1>{content}</h1>"
            )

        elif block_type == "heading_2":

            output.append(
                f"<h2>{content}</h2>"
            )

        elif block_type == "heading_3":

            output.append(
                f"<h3>{content}</h3>"
            )

        # ----------------------------------------------------
        # bulleted list
        # ----------------------------------------------------

        elif block_type == "bulleted_list_item":

            output.append(
                f"<ul><li>{content}</li></ul>"
            )

        # ----------------------------------------------------
        # numbered list
        # ----------------------------------------------------

        elif block_type == "numbered_list_item":

            output.append(
                f"<ol><li>{content}</li></ol>"
            )

        # ----------------------------------------------------
        # quote
        # ----------------------------------------------------

        elif block_type == "quote":

            output.append(
                f"<blockquote>{content}</blockquote>"
            )

        # ----------------------------------------------------
        # divider
        # ----------------------------------------------------

        elif block_type == "divider":

            output.append("<hr>")

        # ----------------------------------------------------
        # code
        # ----------------------------------------------------

        elif block_type == "code":

            code = "".join(
                item.get("plain_text", "")
                for item in rich_text
            )

            language = data.get(
                "language",
                "plain text"
            )

            output.append(
                f'<pre><code class="language-{language}">'
                f'{html.escape(code)}'
                f'</code></pre>'
            )

        # ----------------------------------------------------
        # todo
        # ----------------------------------------------------

        elif block_type == "to_do":

            checked = data.get(
                "checked",
                False
            )

            checkbox = "☑" if checked else "☐"

            output.append(
                f"<p>{checkbox} {content}</p>"
            )

        # ----------------------------------------------------
        # callout
        # ----------------------------------------------------

        elif block_type == "callout":

            icon = data.get("icon") or {}

            emoji = icon.get(
                "emoji",
                "💡"
            )

            output.append(
                f'<div class="callout">'
                f'{emoji} {content}'
                f'</div>'
            )

        # ----------------------------------------------------
        # image
        # ----------------------------------------------------

        elif block_type == "image":

            image_data = (
                data.get("external")
                or data.get("file")
                or {}
            )

            url = image_data.get("url")

            if url:

                output.append(
                    f'<img src="{html.escape(url, quote=True)}" '
                    f'style="max-width:100%;height:auto;">'
                )

    return "\n".join(output)


# ============================================================
# 7. HTML 문서 생성
# ============================================================

def make_html(title, body):

    return f"""<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
        content="width=device-width, initial-scale=1.0">

<title>{html.escape(title)}</title>

<style>

body {{
    font-family:
        Arial,
        "Noto Sans KR",
        sans-serif;

    line-height: 1.7;

    max-width: 900px;

    margin: 40px auto;

    padding: 0 20px;

    color: #333;
}}

h1 {{
    margin-top: 40px;
}}

h2 {{
    margin-top: 30px;
}}

h3 {{
    margin-top: 25px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th,
td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background-color: #f5f5f5;
}}

pre {{
    background-color: #f5f5f5;
    padding: 15px;
    overflow-x: auto;
    border-radius: 5px;
}}

code {{
    font-family: Consolas, monospace;
}}

blockquote {{
    border-left: 4px solid #ccc;
    padding-left: 15px;
    color: #666;
}}

.callout {{
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 6px;
    margin: 15px 0;
}}

img {{
    max-width: 100%;
    height: auto;
}}

</style>

</head>

<body>

{body}

</body>

</html>
"""


# ============================================================
# 8. 부모 페이지의 자식 페이지 찾기
# ============================================================

def get_child_pages():

    blocks = get_blocks(
        NOTION_PARENT_PAGE_ID
    )

    child_pages = []

    for block in blocks:

        if block["type"] == "child_page":

            child_pages.append(block)

    return child_pages


# ============================================================
# 9. 자식 페이지 하나를 HTML로 변환
# ============================================================

def convert_page(page_block, output_dir):

    page_id = page_block["id"]

    title = page_block["child_page"].get(
        "title",
        "untitled"
    )

    print(f"변환 중: {title}")

    # 자식 페이지 본문 가져오기
    blocks = get_blocks(page_id)

    # HTML 변환
    body = blocks_to_html(blocks)

    # HTML 문서 생성
    document = make_html(
        title,
        body
    )

    # 파일명
    filename = make_filename(title)

    output_path = output_dir / filename

    # 저장
    output_path.write_text(
        document,
        encoding="utf-8"
    )

    print(
        f"  → 생성 완료: {output_path}"
    )


# ============================================================
# 10. 실행
# ============================================================

def main():

    # html 폴더 생성
    output_dir = Path("html")

    output_dir.mkdir(
        exist_ok=True
    )

    # 부모 페이지의 자식 페이지 검색
    child_pages = get_child_pages()

    print(
        f"자식 페이지 {len(child_pages)}개 발견"
    )

    # 각각 HTML 생성
    for page in child_pages:

        convert_page(
            page,
            output_dir
        )

    print()
    print("모든 변환이 완료되었습니다.")


if __name__ == "__main__":
    main()