import autogen
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent

config_list = autogen.config_list_from_json('OAI_CONFIG_LIST')

config_list_v4 = autogen.config_list_from_json('OAI_CONFIG_LIST', filter_dict={
    "model": ["gpt-4-vision-preview"]
})

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="You're the boss",
    human_input_mode="NEVER"
)

damage_analyst = MultimodalConversableAgent(
    name="damage_analyst",
    system_message="""
      As the damage analyst your role is to accurately describe the contents of the image provided.
      Respond only with what is visually evident in the image, without adding any additional information or assumptions.
    """,
    llm_config={"config_list": config_list_v4, "max_tokens": 300}
)

inventory_manager = autogen.AssistantAgent(
    name="inventory_mananager",
    system_message="""
      As the inventory manager you provide information about the availability and pricing of spare parts.
      For the time being respond that everything is available.
    """,
    llm_config={"config_list": config_list}
)

customer_support_agent = autogen.AssistantAgent(
    name="customer_support_agent",
    system_message="""
      As a customer support agent you are responsible for drafting emails following confirmation of inventory and pricing. 
      Respond with "TERMINATE" when you have finished.
    """,
    llm_config={"config_list": config_list}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, inventory_manager, customer_support_agent, damage_analyst], messages=[]
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list}
)

user_proxy.initiate_chat(
    manager, message=f"""
      Process Overview:

      Step 1: Damage Analyst identifies the car brand and the requested part 
        (is something central, or something broken or missing?) from the customers message and image

      Step 2: Inventory Manager verifies part availability in the database

      Step 3: Customer Support Agent composes a response email

      Step 4: Colclude the process with sending 'TERMINATE'

      Image Reference: 'https://teslamotorsclub.com/tmc/attachments/camphoto_1144747756-jpg.650059/'
      
    """
)


