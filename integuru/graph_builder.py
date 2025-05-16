from langgraph.graph import END, StateGraph
from integuru.models.agent_state import AgentState
from integuru.agent import IntegrationAgent
from functools import partial  # To pass extra arguments to functions
from integuru.util.print import print_dag, visualize_dag, print_dag_in_reverse

def check_end_condition(state, agent, to_generate_code):
    agent.dag_manager.detect_cycles()

    if len(state.get("to_be_processed_nodes", [])) == 0:
        print("------------------------Successfully analyzed!!!-------------------------------", flush=True)
        print_dag(agent.dag_manager.graph, agent.global_master_node_id)
        visualize_dag(agent.dag_manager.graph)
        print_dag_in_reverse(agent.dag_manager.graph, to_generate_code=to_generate_code)
        return "end"
    else:
        print("Continuing execution", flush=True)
        print(f"Generated graph at current step: {print_dag(agent.dag_manager.graph, agent.global_master_node_id)}", flush=True)
        return "continue"


def build_graph(prompt, har_file_path="network_requests.har", cookie_path="cookies.json", to_generate_code=False):
    agent = IntegrationAgent(prompt, har_file_path, cookie_path)

    graph_builder = StateGraph(AgentState)

    # Add nodes using the agent's methods
    graph_builder.add_node("IntegrationAgent", agent.end_url_identify_agent)
    graph_builder.set_entry_point("IntegrationAgent")

    graph_builder.add_node("urlTocurl", agent.url_to_curl)
    graph_builder.add_edge("IntegrationAgent", "urlTocurl")

    graph_builder.add_node(
        "dynamicurlDataIdentifyingAgent", agent.dynamic_part_identifying_agent
    )
    graph_builder.add_edge("urlTocurl", "dynamicurlDataIdentifyingAgent")

    graph_builder.add_node("inputVariablesIdentifyingAgent", agent.input_variables_identifying_agent)
    graph_builder.add_edge("dynamicurlDataIdentifyingAgent", "inputVariablesIdentifyingAgent")

    graph_builder.add_node("findcurlFromContent", agent.find_curl_from_content)
    graph_builder.add_edge("inputVariablesIdentifyingAgent", "findcurlFromContent")

    # Add conditional edges 
    graph_builder.add_conditional_edges(                
        "findcurlFromContent",
        partial(check_end_condition, agent=agent, to_generate_code=to_generate_code),
        {"end": END, "continue": "dynamicurlDataIdentifyingAgent"},
    )

    graph = graph_builder.compile()
    return graph, agent 
