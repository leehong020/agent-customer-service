from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import before_model, dynamic_prompt, ModelRequest, ToolCallRequest, wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompts,load_report_prompts
from langgraph.runtime import Runtime

# 监控工具调用的中间件
@wrap_tool_call
def monitor_tool(
    #请求的数据封装
    request: ToolCallRequest,
    #执行的函数本身
    handler: Callable[[ToolCallRequest],ToolMessage | Command]
) -> ToolMessage | Command:
    logger.info(f"工具调用监控: 工具名称: {request.tool.name}, 输入参数: {request.tool_call.get('args')}")
    try:
        result = handler(request)
        logger.info(f"工具调用成功: 工具名称: {request.tool.name}") 

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True
        return result
    except Exception as e:
        logger.error(f"工具调用出错: 工具名称: {request.tool.name}, 错误: {e}")
        raise e

@before_model
def log_before_model(
        state:AgentState,
        runtime:Runtime
):
    logger.info(f"模型调用监控: 带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model] {type(state['messages'][-1]).__name__} {state['messages'][-1].content.strip()}")
    
    return None

#动态切换提示词
@dynamic_prompt    #每次提示词生成之前调用此函数
def report_prompt_switch(request:ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report:   #是报告生成场景，返回报告生成提示词内容
        return load_report_prompts()
    return load_system_prompts()   #默认提示词内容
