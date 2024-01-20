import autogen
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from inventory import get_inventory, get_inventory_declaration
from send_mail import send_mail, send_email_declaration
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      image_url = request.form['image']
      customer_email = request.form['email']
      customer_message = request.form['message']

      initiate_chat(image_url, customer_email, customer_message)

      return render_template('result.html')
    else:
       return render_template('index.html')

config_list = autogen.config_list_from_json('OAI_CONFIG_LIST')

config_list_v4 = autogen.config_list_from_json('OAI_CONFIG_LIST', filter_dict={
    "model": ["gpt-4-vision-preview"]
})


def is_termination_msg(data):
    has_content = "content" in data and data["content"] is not None
    return has_content and "TERMINATE" in data["content"]


user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="You're the boss",
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
    function_map={"get_inventory": get_inventory, "send_mail": send_mail}
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
    llm_config={"config_list": config_list,
                "functions": [get_inventory_declaration]}
)

customer_support_agent = autogen.AssistantAgent(
    name="customer_support_agent",
    system_message="""
      As a customer support agent you are responsible for drafting and sending emails following confirmation of inventory and pricing. 
      Respond with "TERMINATE" when you have finished.
    """,
    llm_config={"config_list": config_list, "functions": [send_email_declaration]}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, inventory_manager,
            customer_support_agent, damage_analyst], messages=[]
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": config_list}
)

def initiate_chat(image_url, customer_email, customer_message):
  user_proxy.initiate_chat(
      manager, message=f"""
        Process Overview:

        Step 1: Damage Analyst identifies the car brand and the requested part 
          (is something central, or something broken or missing?) from the customers message and image

        Step 2: Inventory Manager verifies part availability in the database

        Step 3: Customer Support Agent composes and sends a response email

        Customer message: '{customer_message}
        E-Mail of the customer: '{customer_email}
        Image Reference: '{image_url}'
        
      """
  )

if __name__ == '__main__':
    app.run(debug=True)