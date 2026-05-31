from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import anthropic
import os
import io
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SCENES = {
    "official":       ("公文/红头文件",  "正式公文格式，用语庄重规范，遵循国家公文写作标准，措辞准确严谨"),
    "report":         ("工作报告",       "条理清晰，逻辑严密，数据客观，结构规范，层次分明"),
    "wechat_msg":     ("微信消息",       "根据收件方调整语气：给领导语气恭敬简洁；给政府人员正式稳重；给合作方专业友好"),
    "speech":         ("发言稿",         "语气有力，逻辑清晰，节奏感好，适合公开宣读，富有感染力"),
    "ppt":            ("PPT文案",        "标题有力，内容分点清晰，语言精炼，适合幻灯片展示"),
    "work_summary":   ("工作总结",       "成果导向，结构清晰，体现工作价值与贡献，用数字说话"),
    "host":           ("活动主持词",     "流畅自然，衔接顺滑，语气热情专业，过渡语自然得体"),
    "wechat_article": ("微信推文",       "标题吸引人，行文流畅，层次清晰，排版适合微信阅读，结尾有引导"),
    "short_video":    ("短视频脚本",     "口语化表达，节奏紧凑，开头抓人，内容精炼，适合60-90秒口播"),
    "meeting_minutes":("会议纪要",       "客观记录，要点清晰，分议题整理，结论和待办事项突出"),
    "invitation":     ("邀请函",         "措辞得体，说明活动主题/时间/地点，语气正式且诚挚"),
    "press_release":  ("新闻稿",         "客观严谨，导语突出重点，信息完整，适合媒体和公众号发布"),
    "thank_letter":   ("感谢信/贺信",    "情感真诚，语气温暖，措辞得体，体现重视与诚意"),
    "event_plan":     ("活动方案",       "结构完整，目标明确，流程清晰，注意事项周全"),
    "proposal":       ("倡议书",         "立意高远，号召有力，语气积极，体现行业责任感"),
    "survey_notice":  ("调研通知",       "目的清晰，语气礼貌，说明必要性，便于对方理解和配合"),
    "custom":         ("自定义",         "根据用户额外说明灵活处理"),
}

STYLES = {
    "polish":          "整体润色，提升语言质量和表达流畅度，消除语病",
    "shorten":         "精简压缩，去除冗余表达，保持核心意思，控制篇幅",
    "expand":          "适当扩展，增加细节背景论据，丰富内容层次",
    "formalize":       "书面化，用正式规范的表达替换口语化表达，提升文体层次",
    "professionalize": "专业化，融入行业术语和规范表达",
    "vague":           "模糊化，减少过于具体的数字或承诺，表达更有弹性留有余地",
    "precise":         "精确化，表述更具体清晰，关键信息明确，减少歧义",
    "summarize":       "提炼总结核心要点，去粗取精，突出重点",
    "translate":       "中英互译，保持原文语气和专业性，术语翻译准确",
    "outline":         "生成提纲，梳理逻辑结构，列出层级要点框架",
    "format":          "格式整理，重新排版规整，统一标点符号和层级结构",
}


@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.post("/polish")
async def polish(
    text: str = Form(default=""),
    scene: str = Form(default="official"),
    styles: str = Form(default="polish"),
    custom_req: str = Form(default=""),
    recipient: str = Form(default=""),
    file: UploadFile = File(default=None),
):
    file_text = ""
    if file and file.filename:
        raw = await file.read()
        fname = file.filename.lower()
        if fname.endswith(".pdf"):
            file_text = _extract_pdf(raw)
        elif fname.endswith((".docx", ".doc")):
            file_text = _extract_docx(raw)
        elif fname.endswith(".txt"):
            file_text = raw.decode("utf-8", errors="ignore")

    combined = text.strip()
    if file_text.strip():
        combined = (combined + "\n\n【附件内容】\n" + file_text.strip()) if combined else file_text.strip()

    if not combined:
        async def err():
            yield "⚠️ 请输入文字或上传文件"
        return StreamingResponse(err(), media_type="text/plain; charset=utf-8")

    scene_name, scene_desc = SCENES.get(scene, ("自定义", "根据用户要求处理"))
    style_list = [s.strip() for s in styles.split(",") if s.strip()]
    style_descs = "；".join(STYLES.get(s, s) for s in style_list)

    system = (
        "你是一位专业文字助理，服务于连锁经营行业协会的工作人员。"
        "工作背景：用户从事行业协会工作，业务涉及政策沟通、行业协调、会员服务、标准制定、活动组织等。"
        "你的职责：按用户指定的场景和要求处理文字。"
        "输出规范：直接给出处理结果，不加「以下是」「处理后」等引导语，不加解释，不加标题。"
        "语言规范：使用规范简体中文，符合中文行文习惯。"
    )

    user_msg = (
        f"【场景】{scene_name}：{scene_desc}\n"
        f"【处理方式】{style_descs}\n"
        + (f"【发送对象】{recipient}，请据此调整语气、措辞和正式程度\n" if recipient.strip() else "")
        + (f"【额外要求】{custom_req}\n" if custom_req.strip() else "")
        + f"\n【原文】\n{combined}\n\n请直接输出处理结果："
    )

    def stream():
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        ) as s:
            for chunk in s.text_stream:
                yield chunk

    return StreamingResponse(stream(), media_type="text/plain; charset=utf-8")


def _extract_pdf(raw: bytes) -> str:
    try:
        import pypdf
        r = pypdf.PdfReader(io.BytesIO(raw))
        return "\n".join(p.extract_text() or "" for p in r.pages)
    except Exception as e:
        return f"[PDF解析失败：{e}]"


def _extract_docx(raw: bytes) -> str:
    try:
        import docx
        d = docx.Document(io.BytesIO(raw))
        return "\n".join(p.text for p in d.paragraphs if p.text.strip())
    except Exception as e:
        return f"[Word文件解析失败：{e}]"


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8513))
    uvicorn.run(app, host="0.0.0.0", port=port)
