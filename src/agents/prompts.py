from typing import Any, Dict, List
import json


def _format_tool_list(tool_list: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for tool in tool_list:
        lines.append(
            f"- {tool['name']}: {tool['desc']} 参数: {json.dumps(tool['args'], ensure_ascii=False)}"
        )
    return "\n".join(lines)


def explore_tools() -> str:
    tool_list: List[Dict[str, Any]] = [
        {
            "name": "law_retrieval",
            "desc": "法条检索：给定自然语言查询，返回topk最相关的法条。",
            "args": {"query": "str", "topk": "int"},
        },
        {
            "name": "law_recommendation",
            "desc": "法条推荐：给定法条名称（如 刑法第201条），返回相似的法条。",
            "args": {"law": "str"},
        },
        {
            "name": "charge_expansion",
            "desc": "罪名扩展：基于给定罪名列表，返回相似的罪名。",
            "args": {"charges": "List[str]"},
        },
        {
            "name": "case_retrieval",
            "desc": "类案检索：给定检索的类型（民事案件或刑事案件）和案件信息，返回相似的案件。",
            "args": {"type": "str(民事案件|刑事案件)", "query": "str"},
        },
        {
            "name": "template_retrieval",
            "desc": "模板检索：输入文书类型（如：起诉状、答辩状），获取相应的模板。",
            "args": {"template_type": "str(起诉状|答辩状)"}
        },
        {
            "name": "plan_generation",
            "desc": "写作计划生成：根据给定的文书类型，生成写作计划。document_type为文书类型。",
            "args": {"document_type": "str(起诉状|答辩状)"}
        },
        {
            "name": "procedure_retrieval",
            "desc": "流程检索：检索民事/刑事法庭流程。该工具仅在模拟法庭的场景中使用。stage表示阶段，可以检索其中某一阶段，stage=0 为完整流程，民事共有5个阶段，刑事共有3个阶段",
            "args": {"court_type": "str(民事法庭|刑事法庭)", "stage": "int(0-4|0-2)"},
        },
    ]
    return _format_tool_list(tool_list)

def memory_tools() -> str:
    tool_list: List[Dict[str, Any]] = [
        {
            "name": "memory_store",
            "desc": "记忆存储：将关键信息进行储存。记忆类型包括知识存储和上下文存储，content为需要存储的内容。",
            "args": {"memory_type": "str(知识存储|上下文存储)", "content": "Any"}
        },
        {
            "name": "memory_fetch",
            "desc": "记忆读取：从记忆中读取指定类型的记忆。记忆类型包括知识存储和上下文存储。",
            "args": {"memory_type": "str(知识存储|上下文存储)"}
        },
    ]
    memory_store_str = f"- {tool_list[0]['name']}: {tool_list[0]['desc']} 参数: {json.dumps(tool_list[0]['args'], ensure_ascii=False)}"
    memory_fetch_str = f"- {tool_list[1]['name']}: {tool_list[1]['desc']} 参数: {json.dumps(tool_list[1]['args'], ensure_ascii=False)}"
    return memory_store_str, memory_fetch_str

def check_tools() -> str:
    tool_list: List[Dict[str, Any]] = [
        {
            "name": "law_check",
            "desc": "法条内容核查：给定法条名称（如 刑法第201条），返回法条的完整内容。",
            "args": {"law_name": "str"},
        },
        {
            "name": "fact_law_relevance_check",
            "desc": "事实-法条相关性核查：给定事实和法条名称（如 刑法第201条），判断该法条是否适用当前事实。",
            "args": {"fact": "str", "law": "str"},
        },
        {
            "name": "crime_law_consistency_check",
            "desc": "罪名与法条一致性核查：给定罪名和法条名称（如 刑法第201条），验证罪名与刑法法条是否对应。",
            "args": {"crime": "str", "law": "str"},
        },
        {
            "name": "document_format_check",
            "desc": "文书格式检查：给定文书的类型（如：起诉状、答辩状）和文书内容，检查文书格式。注意这里的文书内容要把现有的收集到的完整信息给出，不要遗漏。",
            "args": {"document_type": "str(起诉状|答辩状)", "document": "str"}
        },
        {
            "name": "law_query_rewrite",
            "desc": "法条查询语句改写：给定原始查询语句和案件背景信息，改写查询语句，使其更加明确具体，便于检索相关法条。",
            "args": {"query": "str", "context": "str"},
        },
        {
            "name": "procedure_check",
            "desc": "流程检查：检查民事/刑事法庭流程是否完整。",
            "args": {"court_type": "str(民事法庭|刑事法庭)"},
        },
    ]
    return _format_tool_list(tool_list)


def get_law_thinker_instruction(task: str) -> str:
    tools_text = explore_tools()
    _ , memory_fetch_str = memory_tools()
    example = explore_example(task)
    return f"""
你是一名法律推理助手，能够在必要时调用法律工具获取信息。

【可使用的工具】
{memory_fetch_str}
{tools_text}

【工具调用规范】
当需要调用工具时，请输出以下格式：
<tool_call>{{"name": 工具名, "arguments": JSON参数}}</tool_call>
工具调用的结果会以<tool_call_result>工具调用的结果</tool_call_result>格式输出。

{example}
    """

def explore_example(task: str) -> str:
    if task == "Multi-turn QA":
        return (
            """
在这个任务中，推荐使用记忆读取工具、法条检索、法条推荐工具。
例如：
<tool_call>{"name": "law_retrieval", "arguments": {"query": "当事人提出回避申请需要说明理由吗？", "topk": 5}}</tool_call>
<tool_call_result>系统返回调用相关工具处理后的信息</tool_call_result>
...
            """
        )
    elif task == "Document Generation":
        return (
            """
绝不能虚构“用户的回复：XXX”之类的内容；如果需要用户提供信息，只能向用户提出问题并等待真实回答。
在第一轮对话中，推荐使用模板检索工具和写作计划生成工具。
例如：
<think>...我需要调用模板检索工具，获取该文书类型对应的模板。</think>
<tool_call>{"name": "template_retrieval", "arguments": {"template_type": "起诉状"}}</tool_call>
<tool_call_result>系统返回调用模板检索工具处理后的信息</tool_call_result>
<think>...我需要调用写作计划生成工具，生成一份“需要向用户收集哪些信息”的详细计划。</think>
<tool_call>{"name": "plan_generation", "arguments": {"document_type": "起诉状"}}</tool_call>
<tool_call_result>系统返回调用写作计划生成工具处理后的信息</tool_call_result>
...

在中间轮次对话中，推荐使用记忆读取工具。
例如：
<think>...我需要调用记忆读取工具，从“知识存储”中读取模板与写作计划；并根据计划逐项向用户提问，补齐写文书所需的全部关键信息。</think>
<tool_call>{"name": "memory_fetch", "arguments": {"memory_type": "知识存储"}}</tool_call>
<tool_call_result>系统返回调用记忆读取工具处理后的信息</tool_call_result>
<think>...我需要调用记忆读取工具，从“上下文存储”中读取已经收集到的信息，并根据计划逐项向用户提问未收集到的信息。</think>
<tool_call>{"name": "memory_fetch", "arguments": {"memory_type": "上下文存储"}}</tool_call>
<tool_call_result>系统返回调用记忆读取工具处理后的信息</tool_call_result>
...

在最后一轮对话(进入文书生成阶段)中，推荐使用记忆读取工具。
例如：
<think>...我需要调用记忆读取工具，从“知识存储”中读取模板。</think>
<tool_call>{"name": "memory_fetch", "arguments": {"memory_type": "知识存储"}}</tool_call>
<tool_call_result>系统返回调用记忆读取工具处理后的信息</tool_call_result>
<think>...我需要调用记忆读取工具，从“上下文存储”中读取全部收集到的用户信息。</think>
<tool_call>{"name": "memory_fetch", "arguments": {"memory_type": "上下文存储"}}</tool_call>
<tool_call_result>系统返回调用记忆读取工具处理后的信息</tool_call_result>
...
            """
        )
    elif task == "Court Simulation":
        return (
            """
推荐使用流程检索、法条检索、法条推荐、罪名扩展工具、类案检索工具。
在输出最终判决前必须先完成必要的工具调用以获取到丰富的案件信息和法条知识。

例如：
<think>...我需要调用流程检索工具，获取完整的庭审流程。</think>
<tool_call>{"name": "procedure_retrieval", "arguments": {"court_type": "民事法庭", "stage": 0}}</tool_call>
<tool_call_result>系统返回调用流程检索工具处理后的信息</tool_call_result>
...
<think>...我需要调用法条检索工具，获取相关的法条。</think>
<tool_call>{"name": "law_retrieval", "arguments": {"query": "案件信息", "topk": 5}}</tool_call>
<tool_call_result>系统返回调用法条检索工具处理后的信息</tool_call_result>
...
<think>...我需要调用法条推荐工具，获取相关的法条。</think>
<tool_call>{"name": "law_recommendation", "arguments": {"law": "法条名称"}}</tool_call>
<tool_call_result>系统返回调用法条推荐工具处理后的信息</tool_call_result>
...
<think>...我需要调用罪名扩展工具，获取候选罪名。</think>
<tool_call>{"name": "crime_expansion", "arguments": {"charges": "罪名列表"}}</tool_call>
<tool_call_result>系统返回调用罪名扩展工具处理后的信息</tool_call_result>
...
            """
        )


def get_deep_analysis_prompt(
    reasoning_process: str, user_query: str, tool_used: str, task: str
) -> str:

    tools_text = check_tools()
    memory_store_str, memory_fetch_str = memory_tools()
    examples = check_example(task)

    return f"""
你是一名进行深度分析的法律助手，能够在必要时调用法律工具。你需要基于用户的问题或回复、已有的推理过程和探索阶段的结果进行深度分析。                                                            

【工具调用的基本原则】
1、从核查类工具中选择合适的工具，检查探索阶段获得信息的准确性，以及与用户问题的相关性，是否需要进一步探索其他知识。
2、从推理过程和工具调用结果中总结关键信息，调用记忆存储工具进行存储。

【可使用的工具】
记忆读取工具：
{memory_fetch_str}
记忆存储工具：
{memory_store_str}
核查工具：
{tools_text}

【工具调用格式】
当需要调用工具时，请输出以下格式：
<tool_call>{{"name": 工具名, "arguments": JSON参数}}</tool_call>

{examples}

当前用户的问题或回复：
{user_query}

已有的推理过程：
{reasoning_process}

探索阶段工具调用及结果：
{tool_used}
    """


def check_example(task: str) -> str:
    if task == "Multi-turn QA":
        return (
            """
在这个任务中，推荐使用法条查询语句改写工具、事实-法条相关性核查工具、法条查询语句改写工具和记忆存储工具。
示例：
<think>...我需要检查检索到的法条和用户的问题或回复是否相关。</think>
<tool_call>{"name": "fact_law_relevance_check", "arguments": {"fact": "事实", "law": "检索到的法条名称"}}</tool_call>
<tool_call_result>系统返回调用核查工具的结果</tool_call_result>
<think>...我需要改写查询语句，使其更加明确具体，便于检索相关法条。</think>
<tool_call>{"name": "law_query_rewrite", "arguments": {"query": "原始查询语句", "context": "详细的案件背景信息"}}</tool_call>
<tool_call_result>系统返回调用法条查询语句改写工具处理后的信息</tool_call_result>
<think>...我需要对关键的法律知识进行存储。</think>
<tool_call>{"name": "memory_store", "arguments": {"memory_type": "知识存储", "content": "关键的法律知识：……（具体内容）"}}</tool_call>
<tool_call_result>系统返回调用记忆存储工具处理后的信息</tool_call_result>
<think>...我需要对关键的案件事实进行存储。</think>
<tool_call>{"name": "memory_store", "arguments": {"memory_type": "上下文存储", "content": "关键的案件事实：……（具体内容）"}}</tool_call>
<tool_call_result>系统返回调用记忆存储工具处理后的信息</tool_call_result>
...
            """
        )
    elif task == "Document Generation":
        return (
            """
在第一轮对话中，推荐使用记忆存储工具。
例如：
<think>...我需要把检索到的文书模版（或生成的写作计划）进行存储。</think>
<tool_call>{"name": "memory_store", "arguments": {"memory_type": "知识存储", "content": "检索到的文书模版（或生成的写作计划）：……（具体内容）"}}</tool_call>
<tool_call_result>系统返回调用记忆存储工具处理后的信息</tool_call_result>
...

在中间轮次对话中，推荐使用记忆读取工具和记忆存储工具。
例如：
<think>...我需要调用记忆读取工具，从“知识存储”中读取检索到的文书模版。</think>
<tool_call>{"name": "memory_fetch", "arguments": {"memory_type": "知识存储"}}</tool_call>
<tool_call_result>系统返回调用记忆读取工具处理后的信息</tool_call_result>
<think>...我需要调用记忆存储工具，将已经收集到的信息进行存储。</think>
<tool_call>{"name": "memory_store", "arguments": {"memory_type": "上下文存储", "content": "已经收集到的信息：……（具体内容）"}}</tool_call>
<tool_call_result>系统返回调用记忆存储工具处理后的信息</tool_call_result>
...

最后一轮对话中（进入文书生成阶段），推荐使用文书格式检查工具，这个工具非常重要，一定要检查清楚。
例如：
<think>...我要对生成文书的格式进行检查。</think>
<tool_call>{"name": "document_format_check", "arguments": {"document_type": "起诉状", "document": "生成的文书内容"}}</tool_call>
<tool_call_result>系统返回调用文书格式检查工具处理后的信息</tool_call_result>
...
            """
        )
    elif task == "Court Simulation":
        return (
            """
推荐使用法条查询语句改写工具、法条内容核查工具、法条推荐工具、流程检查工具和记忆存储工具。

例如：
<think>...我需要调用流程检查工具，检查当前阶段的庭审流程是否完整。</think>
<tool_call>{"name": "procedure_check", "arguments": {"court_type": "民事法庭"}}</tool_call>
<tool_call_result>系统返回调用流程检查工具处理后的信息</tool_call_result>
...
<think>...我要对检索到的法条进行核查。</think>
<tool_call>{"name": "law_check", "arguments": {"law_name": "检索到的法条名称"}}</tool_call>
<tool_call_result>系统返回调用核查工具处理后的信息</tool_call_result>
...
<think>...我需要改写查询语句，使其更加明确具体，便于检索相关法条。</think>
<tool_call>{"name": "law_query_rewrite", "arguments": {"query": "原始查询语句", "context": "详细的案件背景信息"}}</tool_call>
<tool_call_result>系统返回调用法条查询语句改写工具处理后的信息</tool_call_result>
<think>...我需要调用法条推荐工具，看是否还有更合适的相关法条。</think>
...
<think>...我需要调用法条推荐工具，看是否还有更合适的相关法条。</think>
<tool_call>{"name": "law_recommendation", "arguments": {"law": "检索到的法条名称"}}</tool_call>
<tool_call_result>系统返回调用法条推荐工具处理后的信息</tool_call_result>
...
            """
        )

def get_response_prompt_qa(system_prompt: str, question: str, output: str) -> str:
    return (
        """
你是一名法律助手，基于已有的推理过程，进行总结，生成回复的对话内容。请严格遵循以下规范：
在对话中你的身份是：{system_prompt}
用户的问题：{question}
已有的推理过程：{output}
        """
    ).format(system_prompt=system_prompt, question=question, output=output)
#     return (
#         """
# 你是一名专业法律助手，请基于下面的“推理过程”精准地回复用户。
# 【你的身份】
# {system_prompt}

# 【用户提问】
# {question}

# 【推理过程】
# {output}

# 请遵循所有要求：
# （1）先通读推理过程，提炼可直接回答用户的问题的关键信息，再组织回复；不要逐句复述推理。
# （2）若问题为“是否 / 能否”类，请给出明确结论（“是”或“否”），并简要说明理由。
# （3）若问题涉及具体法条，请列出所有相关法条原文及关键条款编号，避免遗漏。
#         """
#     ).format(system_prompt=system_prompt, question=question, output=output)


def get_response_prompt_report(system_prompt: str, output: str, document_type: str) -> str:
    if document_type == "起诉状":
        return (
            """
你是一名法律助手，基于已有的推理过程，进行总结，生成回复的对话内容。请严格遵循以下规范：
在对话中你的身份是：{system_prompt}
已有的推理过程：{output}
注意：
（1）直接生成回复内容，不要使用“以下是生成的对话内容：”等提示性前缀。
（2）只有在最终输出完整的法律文书后，才允许使用标记 <询问结束>，绝不能提前输出此标记。
（3）文书格式
- 必须严格按照下列字段名输出，字段名必须完全一致（全角中文冒号“：”）：
    - 标题：民事起诉状
    - 原告：
    - 被告：
    - 诉讼请求：
    - 事实和理由：
    - 证据和证据来源，证人姓名和住所：
- 禁止出现任何带括号的可选说明，例如 “原告（如果是自然人）：”、“被告（如果是自然人）：”等形式。
- 禁止使用任何文本加粗或 MarkDown 风格（如 **原告**：）。所有文本应为纯文本文字。
- 禁止在字段名后使用逗号替代冒号，必须使用“：”。
            """
        ).format(system_prompt=system_prompt, output=output)
        
    elif document_type == "答辩状":
        return (
            """
    你是一名法律助手，基于已有的推理过程，进行总结，生成回复的对话内容。请严格遵循以下规范：
    在对话中你的身份是：{system_prompt}
    已有的推理过程：{output}
    注意：
    （1）直接生成回复内容，不要使用“以下是生成的对话内容：”等提示性前缀。
    （2）只有在最终输出完整的法律文书后，才允许使用标记 <询问结束>，绝不能提前输出此标记。
    （3）文书格式
    - 严格按照下列字段名格式输出（全角中文冒号“：”）：
        - 标题：民事答辩状
        - 答辩人：
        - 对**人民法院**民初**号**一案的起诉，答辩如下：
        - 证据和证据来源，证人姓名和住所：
    - 其中 “对**人民法院**民初**号**一案的起诉，答辩如下：” 中的 ** 必须根据案件实际内容替换为具体信息；其余所有文字必须保持完全不变。
    - 禁止出现任何带括号的可选说明，例如 “答辩人（如果是法人）：”等形式。
            """
        ).format(system_prompt=system_prompt, output=output)

def get_response_prompt_judge(system_prompt: str, output: str, court_type: str) -> str:
    if court_type == "民事法庭":
        end = """注意：
在每一个阶段开始时，先说明当前所处的阶段（开庭审理、法庭调查、庭审辩论、法庭调解），不要提及其他阶段。
在每一轮对话中，只可以对一个用户扮演的角色发言，当你想要对原告发言时，在对话开头使用“对原告说：”，此时不能对被告发言。当你想要对被告发言时，在对话开头使用“对被告说：”，此时不能对原告发言。当你不想对任何用户扮演角色发言时，不要在对话开头使用“对原告说：”和“对被告说：”。
无论是否同意调解，都要进行最终宣判。禁止在法庭调解结束后直接输出<结束庭审>。
"""

    elif court_type == "刑事法庭":
        end = """注意：
在每一个阶段开始时，先说明当前所处的阶段（开庭审理、法庭调查、最终宣判），不要提及其他阶段。
在每一轮对话中，只可以对一个用户扮演的角色发言，当你想要对被告当事人发言时，在对话开头使用“对被告当事人说：”，此时不能对其他角色发言。当你想要对被告辩护人发言时，在对话开头使用“对被告辩护人说：”，此时不能对其他角色发言。当你想要对公诉机关发言时，在对话开头使用“对公诉机关说：”，此时不能对其他角色发言。当你不想对任何用户扮演角色发言时，不要在对话开头使用“对被告当事人说：”、“对被告辩护人说：”和“对公诉机关说：”。每一轮只能对一个用户扮演角色发言。"
"""

    return (
        """
你是一名法律助手，基于已有的推理过程，进行总结，生成回复的对话内容。请严格遵循以下规范：
在对话中你的身份是：{system_prompt}
已有的推理过程：{output}
{end}
        """
    ).format(system_prompt=system_prompt, output=output, end=end, court_type=court_type)
