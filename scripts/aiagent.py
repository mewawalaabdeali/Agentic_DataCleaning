import openai
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("API Key missing. Environment variable not set.")

llm = OpenAI(openai_api_key=openai_api_key, temperature=0)

class CleaningState(BaseModel):
    """State Schema for LangGraph: manages input prompt and structured response."""
    input_text : str
    structured_response: str

class AIAgent:
    def __init__(self):
        """Initialize the LangGraph cleaning agent"""
        self.graph = self._create_graph()

    def _create_graph(self):
        """Defines the LangGraph Workflow"""
        graph = StateGraph(CleaningState)

        def agent_logic(state:CleaningState) -> CleaningState:
            response = llm.invoke(state.input_text)
            return CleaningState(input_text=state.input_text, structured_response=response)
        
        graph.add_node("cleaning_agent", agent_logic)
        graph.add_edge("cleaning_agent", END)
        graph.set_entry_point("cleaning_agent")
        return graph.compile()
    
    def process_data(self, df:pd.DataFrame, batch_size=20) -> str:
        """Process a dataframe in batches and returns the cleaned data as text"""
        cleaned_response = []

        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i + batch_size]
            prompt=f"""
            You are an AI Data Cleaning Agent with MLOps Expertise. Analyze the dataset below:
            
            {df_batch.to_markdown(index=False)}
            
            Instructions:
            1. Identify missing values and impute them using mean, median or mode.
            2. Remove duplicates
            3. Format all dates and categorical text columns properly.
            
            Return only the cleaned table."""

            state = CleaningState(input_text=prompt, structured_response="")
            response = self.graph.invoke(state)

            if isinstance(response, dict):
                response= CleaningState(**response)

            if not response.structured_response.strip():
                cleaned_response.append("[ERROR] Empty response from LLM")
            else:
                cleaned_response.append(response.structured_response)
        return "\n".join(cleaned_response)
    
    def save_to_file(self, output_text:str, file_path="outputs/cleaned_output.txt"):
        """Saves the cleaned result to a text file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"Cleaned Data saved to {file_path}")

if __name__=="__main__":
    sample_data=pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, None],
        "salary": [50000, 60000, 55000],
        "joined": ["2022-01-01", "2022-01-02", "not_a_date"]
    })

    agent = AIAgent()
    cleaned = agent.process_data(sample_data)
    agent.save_to_file(cleaned)