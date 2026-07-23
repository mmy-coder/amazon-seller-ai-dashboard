"""
AI 服务层 —— 调用 DeepSeek API 或返回 Mock 数据

设计原则：
- 优先从环境变量读取 DEEPSEEK_API_KEY
- 没有 API Key 时使用 mock 数据，确保项目可以正常运行
- 所有 AI 函数统一返回结构化的 dict

DeepSeek API 的 base URL：https://api.deepseek.com/v1
"""

import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)
DEEPSEEK_API_KEY = settings.deepseek_api_key
DEEPSEEK_BASE_URL = settings.deepseek_base_url


def _has_api_key() -> bool:
    """检查是否有可用的 API Key"""
    return bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your_deepseek_api_key_here")


async def _call_deepseek(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    """
    调用 DeepSeek API

    Args:
        prompt: 用户提示词
        system_prompt: 系统提示词

    Returns:
        API 返回的文本内容
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 2048,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


def _mock_review_analysis() -> dict:
    """Mock 评论分析结果（无 API Key 时使用）"""
    return {
        "_source": "mock",
        "_warning": "未配置 DeepSeek API Key，当前展示演示数据。",
        "pain_points": "1. 电池续航不足，使用2-3小时后需要充电\n"
                        "2. 风力不够大，户外炎热天气效果不佳\n"
                        "3. 噪音偏大，安静场合使用尴尬\n"
                        "4. 重量偏重，长时间佩戴不舒服",
        "positive_points": "1. 外观设计时尚，颜色选择多\n"
                           "2. 价格实惠，性价比高\n"
                           "3. 便携性好，适合通勤使用\n"
                           "4. 充电速度快，Type-C 充电方便",
        "negative_points": "1. 续航严重不足（出现频率最高）\n"
                           "2. 最大档位噪音大\n"
                           "3. 材质塑料感强，质感一般\n"
                           "4. 售后服务响应慢",
        "improvement_suggestions": "1. 升级电池容量至 4000mAh 以上，延长续航至6小时\n"
                                   "2. 优化扇叶设计，降低高档位噪音\n"
                                   "3. 采用亲肤材质和人体工学设计，减轻重量\n"
                                   "4. 增加风量档位显示和智能温控功能",
        "listing_suggestions": "1. 标题突出「超长续航6小时+超静音」，解决用户核心痛点\n"
                              "2. 五点描述第一条强调电池升级和降噪技术\n"
                              "3. A+页面展示续航和噪音对比图\n"
                              "4. 主图增加使用场景图（办公/通勤/户外）",
        "selling_points": "1. 升级4800mAh大电池，续航长达6小时\n"
                          "2. 超静音设计，低于40分贝\n"
                          "3. 无叶安全设计，适合长发和儿童\n"
                          "4. 多场景适用：办公、通勤、户外、运动\n"
                          "5. 人体工学轻量化设计，长时间佩戴不疲劳",
    }


def _mock_listing_optimization(product_name: str = "", category: str = "") -> dict:
    """Mock Listing 优化结果（无 API Key 时使用）"""
    return {
        "_source": "mock",
        "_warning": "未配置 DeepSeek API Key，当前展示演示数据。",
        "title_suggestions": f"【2025升级款】{product_name} - 超长续航|静音设计|便携式 - 适用于办公/户外/通勤\n"
                             f"备选：{product_name} | 4800mAh大电池 | 3档风速 | 无叶安全设计 | 轻量化便携",
        "bullet_points": f"【超长续航】升级4800mAh大容量电池，一次充电可使用6-8小时，告别电量焦虑；Type-C快充接口，充电更方便\n\n"
                         f"【超静音设计】采用第3代无刷电机和优化的扇叶结构，运行噪音<40dB，即使在安静的办公室也不会打扰他人\n\n"
                         f"【3档智能风速】低档柔和自然风、中档清爽舒适风、高档强劲降温风，满足不同场景需求；一键切换，简单易用\n\n"
                         f"【无叶安全设计】无外露叶片，安全不伤手；特别适合长发用户和家有小孩的家庭；清洁方便，一擦即净\n\n"
                         f"【轻量化人体工学】仅重180g，食品级亲肤硅胶材质，弧度可调适配不同颈围，长时间佩戴也不疲劳",
        "search_keywords": f"{product_name}, neck fan, portable fan, rechargeable fan, hands-free fan, "
                           f"personal fan, USB fan, wearable fan, outdoor cooling, travel fan, "
                           f"quiet fan, bladeless fan, summer essentials, office fan, camping gear",
        "product_description": f"<h3>告别炎热，随时随地享受清凉</h3>\n"
                               f"<p>这款{product_name}是2025年全新升级款，专为现代都市人打造。"
                               f"无论是通勤路上、办公室午休、户外露营还是健身运动，它都是您的最佳伴侣。</p>\n"
                               f"<h3>为什么选择我们？</h3>\n"
                               f"<ul><li>4800mAh大电池，续航碾压同类产品</li>"
                               f"<li>第3代静音技术，图书馆也能用</li>"
                               f"<li>无叶安全设计，全家都能放心使用</li>"
                               f"<li>180g轻量化，挂脖无负担</li></ul>",
        "differentiation_points": f"1. 续航差异化：主推「6小时+超长续航」，这是用户评论中最大的痛点，市面上多数产品仅2-3小时\n"
                                    "2. 静音差异化：主推「<40dB静音运行」，适合办公和学习场景，扩大目标用户群\n"
                                    "3. 安全差异化：主推「无叶设计+亲肤材质」，吸引有孩家庭和长发女性用户\n"
                                    "4. 颜值差异化：推出多配色选择，打造「时尚配饰」属性而非单纯的「工具属性」",
    }


async def analyze_reviews(reviews: str) -> dict:
    """
    AI 评论分析

    输入一批用户评论，AI 提取：
    - 用户主要痛点
    - 高频好评点
    - 高频差评点
    - 产品改进建议
    - Listing 优化建议
    - 可提炼的卖点

    Args:
        reviews: 用户粘贴的评论文本（多行文本）

    Returns:
        dict: 分析结果
    """
    # 没有 API Key 时使用 mock 数据
    if not _has_api_key():
        return _mock_review_analysis()

    # 构建发送给 AI 的提示词（prompt）
    prompt = f"""请分析以下 Amazon 用户评论，用中文输出分析结果。

评论内容：
{reviews}

请按以下格式输出：
1. 用户主要痛点（列出每条，格式：痛点描述）
2. 高频好评点（列出每条）
3. 高频差评点（列出每条）
4. 产品改进建议（列出每条，要具体可执行）
5. Listing 优化建议（列出每条）
6. 可以提炼进五点描述的卖点（列出5条，每条用英文关键词标注）

请确保分析基于评论文本，不要编造内容。"""

    try:
        ai_response = await _call_deepseek(prompt, "你是一位 Amazon 跨境电商产品分析专家。")
        # 将 AI 返回的文本解析为结构化字段（简化处理）
        return {
            "_source": "deepseek",
            "_warning": "",
            "pain_points": _extract_section(ai_response, "痛点"),
            "positive_points": _extract_section(ai_response, "好评"),
            "negative_points": _extract_section(ai_response, "差评"),
            "improvement_suggestions": _extract_section(ai_response, "改进"),
            "listing_suggestions": _extract_section(ai_response, "Listing"),
            "selling_points": _extract_section(ai_response, "卖点"),
        }
    except Exception as exc:
        logger.exception("DeepSeek 评论分析失败，已降级为演示数据: %s", exc)
        result = _mock_review_analysis()
        result["_warning"] = "DeepSeek 调用失败，当前展示演示数据，请检查 API 配置或网络。"
        return result


async def optimize_listing(
    product_name: str,
    category: str = "",
    core_selling_points: str = "",
    target_users: str = "",
    competitor_weakness: str = "",
    user_pain_points: str = "",
) -> dict:
    """
    AI Listing 优化

    根据商品信息、竞品弱点、用户痛点，生成优化的 Listing 内容。

    Returns:
        dict: 包含标题、五点描述、关键词、产品描述、差异化卖点
    """
    # 没有 API Key 时使用 mock 数据
    if not _has_api_key():
        return _mock_listing_optimization(product_name, category)

    # 构建 AI 提示词
    prompt = f"""你是一位专业的 Amazon Listing 优化专家。请根据以下信息为产品生成优化的 Listing 内容。

## 产品信息
- 商品名：{product_name}
- 类目：{category or "未提供"}
- 核心卖点：{core_selling_points or "未提供"}
- 目标用户：{target_users or "未提供"}

## 竞品弱点
{competitor_weakness or "未提供"}

## 用户痛点
{user_pain_points or "未提供"}

请用中文生成以下内容：
1. Amazon 标题建议（2个版本，每个标题不超过200字符，包含核心关键词）
2. 五点描述（5条，每条以【核心卖点】开头，要符合 Amazon 的格式要求）
3. 搜索关键词（列出15-20个英文关键词，用逗号分隔）
4. 产品描述（HTML格式，包含h3标题和ul列表）
5. 差异化卖点（基于竞品弱点提出3-5条差异化策略）

请确保输出内容符合 Amazon 的 Listing 规范，使用地道的 Amazon 卖家语言风格。"""

    try:
        ai_response = await _call_deepseek(prompt, "你是一位 Amazon 跨境电商 Listing 优化专家。")
        return {
            "_source": "deepseek",
            "_warning": "",
            "title_suggestions": _extract_section(ai_response, "标题"),
            "bullet_points": _extract_section(ai_response, "五点描述|bullet"),
            "search_keywords": _extract_section(ai_response, "关键词"),
            "product_description": _extract_section(ai_response, "产品描述|描述"),
            "differentiation_points": _extract_section(ai_response, "差异化"),
        }
    except Exception as exc:
        logger.exception("DeepSeek Listing 优化失败，已降级为演示数据: %s", exc)
        result = _mock_listing_optimization(product_name, category)
        result["_warning"] = "DeepSeek 调用失败，当前展示演示数据，请检查 API 配置或网络。"
        return result


def _extract_section(text: str, keyword: str) -> str:
    """
    从 AI 返回的文本中提取某个章节内容（简易版）

    真实项目中会用更结构化的方式（如要求 AI 返回 JSON），
    这里做简单的文本提取以保证可用性。
    """
    import re
    # 尝试匹配 "1. 关键词：" 或 "## 关键词" 格式的内容
    pattern = rf"(?:^|\n).*?{keyword}.*?[:：](.*?)(?:\n.*?(?:\d+\.|#)|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        content = match.group(1).strip()
        return content[:2000]  # 限制长度
    # 如果匹配不到，返回原始文本的一部分
    return text[:500] if len(text) > 500 else text
