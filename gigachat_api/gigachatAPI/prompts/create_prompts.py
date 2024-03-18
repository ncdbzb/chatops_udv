from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, load_prompt


async def create_prompt(path_system: str, path_user: str = '') -> ChatPromptTemplate:
    if path_user:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(
                    prompt=load_prompt(path_system)
                ),
                HumanMessagePromptTemplate(
                    prompt=load_prompt(path_user)
                )
            ]
        )
    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(
                prompt=load_prompt(path_system)
            )
        ]
    )


