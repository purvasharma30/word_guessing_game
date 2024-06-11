from autogen import config_list_from_json
import autogen

# Importing OPENAI API KEY
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config={ "config_list" : config_list
            , "request_timeout" : 120}

# Creating User Proxy Agent
user_proxy_agent = autogen.UserProxyAgent( name="user_proxy_agent"
                                  ,system_message="This is Human admin who will give idea and feedback on the code provided by Coder. Once user press ENTER, code will run."
                                  ,code_execution_config={ "last_n_messages":2, "work_dir":"new_game"}
                                  ,human_input_mode="ALWAYS")

# Creating coder Agent
coder = autogen.AssistantAgent(name="Coder"
                            , system_message=" Write the code according to the requirements given by pm. Run and Debug the code and Fix the errors. Install required libraries whenever required."
                            ,llm_config=llm_config
                            )

# Product Manager Agent
pm = autogen.AssistantAgent(
    name="product_manager"
    , system_message="You will help breakdown the initial idea into a well scoped requirement for the Coder. Do not invlove in future conversations or error fixing."
    , llm_config=llm_config
)


# Create a groupchat
groupchat= autogen.GroupChat(
    agents = [user_proxy_agent, coder, pm],
    messages=[]
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the conversation
user_proxy_agent.initiate_chat(
    manager, message="Build a Word guessing game. In this game, there is a list of words present, out of which our interpreter will choose 1 random word. The user first has to input their names and then, will be asked to guess any alphabet. If the random word contains that alphabet, it will be shown as the output(with correct placement) else the program will ask you to guess another alphabet. The user will be given 12 turns(which can be changed accordingly) to guess the complete word."
)
